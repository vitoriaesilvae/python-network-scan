"""
Esse módulo contém funções para realizar varreduras de rede e gerar relatórios dos resultados. 
Ele utiliza programação assíncrona para melhorar a eficiência do scan, permitindo que múltiplos hosts e portas sejam verificados simultaneamente.
Aqui estão as principais funcionalidades:
- ping_sweep: Realiza um sweep de ping em uma rede para identificar hosts ativos.
- scan_port: Verifica se uma porta específica está aberta em um host.
- grab_banner: Tenta capturar o banner de um serviço em uma porta aberta.
- dns_reverso: Realiza uma consulta de DNS reverso para obter o hostname de um IP.
- scan_host: Escaneia todas as portas comuns de um host ativo e coleta informações sobre serviços e banners.
- run_scan: Coordena o processo de varredura, combinando ping sweep e scan de portas, e gera relatórios em JSON, CSV e HTML.
"""
import sys 
import report
import utils
import time #biblioteca para medir o tempo de execução do scan
import asyncio #biblioteca para programação assíncrona
import ipaddress
import socket

PORTAS_COMUNS = range(1,1000)
PORTAS_QUE_PRECISAM_DE_REQUISICAO = {80}

async def ping_host(ip):
    #O await indica ao python para adiantar outras tarefas assíncronas enquanto essa não termina
    #create_subprocess_exec roda uma tarefa no OS, o final _exec indica que vai passar o comando como uma lista de strings.
    processo = await asyncio.create_subprocess_exec(
        "ping", "-c", "1", "-W", "1", str(ip),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    #.wait indica ao python para esperar até o fim do processo
    await processo.wait()
    return processo.returncode == 0

async def ping_sweep(rede, concorrencia=100):
    rede_obj = ipaddress.ip_network(rede, strict=False)
    ips = list(rede_obj.hosts())

    #o semáforo é um limitador de tarefas simultaneas do asyncio
    semaforo = asyncio.Semaphore(concorrencia)

    async def teste(ip):
        async with semaforo:
            ativo = await ping_host(ip)
            if ativo:
                print(f"Host ativo: {ip}")
            return str(ip) if ativo else None
        
    resultados = await asyncio.gather(*(teste(ip) for ip in ips))
    return [ip for ip in resultados if ip is not None]

async def scan_port(ip, porta, timeout=1):
    try:
        conexao = asyncio.open_connection(ip, porta)
        reader, writer = await asyncio.wait_for(conexao, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except(asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False

async def grab_banner(ip, porta, timeout=2):
    try:
        conexao = asyncio.open_connection(ip, porta)
        #reader e writer são objetos de stream do asyncio, que permitem ler e escrever dados de forma assíncrona.
        #o wait_for é usado para limitar o tempo de espera da conexão, caso contrário o scan poderia travar indefinidamente em portas que não respondem.
        reader, writer = await asyncio.wait_for(conexao, timeout=timeout)

        if porta in PORTAS_QUE_PRECISAM_DE_REQUISICAO:
            requisicao = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Scan\r\nConnection: close\r\n\r\n"
            #writer.write() escreve os dados no stream de saída, e o encode() converte a string em bytes, que é o formato esperado pelo writer.
            writer.write(requisicao.encode())
            #writer.drain() é usado para garantir que todos os dados foram enviados antes de continuar, caso contrário o scan poderia falhar em portas que demoram para responder.
            await writer.drain()
        
        dados = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        writer.close()
        #writer.wait_closed() é usado para garantir que a conexão foi fechada corretamente, caso contrário o scan poderia deixar conexões abertas no sistema.
        await writer.wait_closed()

        #o strip() remove espaços em branco e quebras de linha do início e do fim da string.
        banner = dados.decode(errors="ignore").strip()
        #retorna o banner se ele não for vazio, caso contrário retorna None.
        return banner if banner else None
    except(asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None

async def dns_reverso(ip, portas=None, concorrencia_port=50):
    #get_running_loop() retorna o loop de eventos atual do asyncio, que é necessário para rodar funções de bloqueio como socket.gethostbyaddr() em um executor.
    #funções de bloqueio são aquelas que podem demorar para retornar, como operações de rede ou de disco, e podem travar o loop de eventos se não forem executadas em um executor.
    loop = asyncio.get_running_loop()
    
    try:
        #O underlinne _ é uma convenção para indicar que a variável não será usada, nesse caso o endereço IP retornado por gethostbyaddr() não é necessário, apenas o hostname.
        hostname, _, _ = await asyncio.wait_for(
            loop.run_in_executor(None, socket.gethostbyaddr, ip),
            timeout=2)
        return hostname
    #socket.herror é levantado quando o hostname não pode ser resolvido, e socket.gaierror é levantado quando o endereço IP não é válido.
    except(socket.herror, socket.gaierror):
        return None
    
async def scan_host(ip, portas=None, concorrencia_port=100):
    if portas is None:
        portas = PORTAS_COMUNS

    semaforo = asyncio.Semaphore(concorrencia_port)

    async def teste_porta(porta):
        async with semaforo:
            aberta = await scan_port(ip,porta)
            if not aberta:
                return None
            else:
                servico = utils.obter_servico(porta)
                banner = await grab_banner(ip, porta)
                return {"porta": porta, "servico": servico, "banner": banner}
        
    resultados = await asyncio.gather(*(teste_porta(p) for p in portas))
    return [r for r in resultados if r is not None]

async def scan_single_host(ip):
    hostname = await dns_reverso(ip)
    portas = await scan_host(ip)

    return {"host": ip, "hostname": hostname, "portas": portas}

async def run_scan(rede, concorrencia_hosts=10):
    hosts_ativos = await ping_sweep(rede)

    semaforo = asyncio.Semaphore(concorrencia_hosts)

    async def processar(ip):
        async with semaforo:
            return await scan_single_host(ip)
        
    print("\nEscaneando portas...")  
    resultados = await asyncio.gather(*(processar(ip) for ip in hosts_ativos))

    return resultados

async def main():
    if len(sys.argv) != 2:
        print("Uso: python3 scanner_async.py <rede>")
        print("Exemplo: python3 scanner_async.py 192.168.1.0/24")
        sys.exit(1)

    rede_alvo = sys.argv[1]

    print(f"Iniciando scan em {rede_alvo}...\n")
    inicio = time.time()

    resultados = await run_scan(rede_alvo)

    duracao = time.time() - inicio

    dados_relatorio = {"hosts": resultados}

    report.gerar_relatorio_json(dados_relatorio)
    report.gerar_relatorio_csv(dados_relatorio)
    report.gerar_relatorio_html(dados_relatorio)

    print(f"\nHosts escaneados: {len(resultados)}")
    print(f"Tempo total: {duracao:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())


