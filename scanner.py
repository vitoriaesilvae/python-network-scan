"""
Esse módulo ficará responsável por chamar os outros módulos para realizar a varredura de portas, coletar banners e nomes de domínio, e organizar os resultados em um relatório final.
Uso para teste: 
python3 scanner.py [ip]
"""
import sys #biblioteca que permite acessar informações e funcionalidades do interpretador python.
import ping
import port_scanner 
import banner
import dns
import report
import utils

def run_scan(rede):

    resultados = {} 

    #descobrir hosts ativos
    hosts_ativos = ping.ping_sweep(rede)

    #Monta o dicionário para cada host ativo.
    for host in hosts_ativos:
        resultados[host] = {}

        #Varre as portas do host ativo.
        portas_abertas = port_scanner.scan_host(host)

        #Para cada porta aberta, coleta o banner e o nome de domínio.
        for porta in portas_abertas:
            banner_servico = banner.banner_grabbing(host, porta)
            nome_dominio = dns.obter_nome_dominio(host)

            #Adiciona os resultados ao dicionário.
            resultados[host][porta] = {
                "servico": utils.obter_servico(porta),
                "banner": banner_servico,
                "nome_dominio": nome_dominio
            }

    #O código abaixo junta os resultados de todos os hosts ativos em um único dicionário, que será usado pelo report.py para gerar o relatório final.
    resultados_finais = {}
    for host, portas in resultados.items():
        resultados_finais[host] = portas

    return resultados_finais

#O código abaixo envia os resultados para o report.py gerar o relatório final, e só será executado se o arquivo for executado diretamente, e não importado como módulo.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 scanner.py <ip>")
        print("Exemplo: python3 scanner.py 192.168.0.1")
        sys.exit(1)

    ip = sys.argv[1]
    resultados = run_scan(ip)
    report.gerar_relatorio_csv(resultados)
    report.gerar_relatorio_html(resultados)
    report.gerar_relatorio_json(resultados)
