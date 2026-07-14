"""
Ping sweep

Objetivo: Descobrir quais ips de uma rede estão ativos.

Execução para teste : python3 ping.py [endereço de rede]

Otimização: O ping sweep é feito em paralelo, usando threads, para acelerar o processo.
"""

import ipaddress  #biblioteca responsável pela interpretação endereço  de rede e gerar todos os IPs pertencentes à ela. 
import subprocess #biblioteca que permite usar comandos do sistema operacional pelo python.
import sys #biblioteca que permite a leitura dos argumentos da linha de comando.

def ping_host(ip):
	"""
	Realiza o ping em um ip.
	Retorna true se o host respondeu, false se não.
	"""
	comando = ["ping", "-c","1", "-W", "1", str(ip)]

	"""
	subprocess.run() executa o comando acima e espera terminar.
	stdout = saída padrão  | stderr = saída de erros 
	.DEVNULL envia as saídas para o buraco negro do linux (a pasta /dev/null)
	"""
	resultado = subprocess.run(
		comando,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL )

	#returncode == 0 significa que se o ping teve resposta ele retornará 0.
	return resultado.returncode == 0


def ping_sweep_threaded(rede, max_workers=100): 
	#Recebe um string de rede e retorna uma lista de IPs que responderam ao ping, usando threads para acelerar o processo.
	from concurrent.futures import ThreadPoolExecutor #biblioteca que permite criar threads para executar funções em paralelo.

	hosts_ativos = []
	rede_obj = ipaddress.ip_network(rede, strict=False)
	ips = list(rede_obj.hosts())

	#O ThreadPoolExecutor cria uma pool de threads reutilizáveis.
	#O with garante que todas as threads serão encerradas corretamente, mesma lógica usada em report.py
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		#O executor.map distribui o trabalho para as threads, cada uma executando o ping_host com um ip da lista ips.
		#resultados contém a lista dos resultados dos pings, com true ou false.
		resultados = executor.map(ping_host,ips)

		#o zip permite varrer duas listas ao mesmo tempo
		for ip, ativo in zip(ips, resultados):
			if ativo:
				print(f"Host ativo: {ip}")
				hosts_ativos.append(str(ip))
		
	print("\n")
	return hosts_ativos


#O código abaixo roda apenas se esse arquivo for executado sozinho
if __name__ == "__main__":
	if len(sys.argv) != 2: #sys.argv guarda os argumentos digitados no terminal em uma lista, separando os itens pelo espaço.
		print("Uso: python3 ping.py [rede]")
		print("Exemplo: python3 ping.py 192.168.1.0/24")
		sys.exit(1) #fecha o programa com o código de erro 1.

	rede_alvo = sys.argv[1] #guarda o segundo argumento digitado (o endereço de rede) na variável.

	print(f"Iniciando ping sweep em {rede_alvo}...\n")
	ativos = ping_sweep_threaded(rede_alvo) 

	print(f"\nTotal de hosts ativos: {len(ativos)}")
	for ip in ativos:
		print(f" - {ip}")
