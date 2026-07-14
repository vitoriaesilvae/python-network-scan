"""
Ping sweep

Objetivo: Descobrir quais ips de uma rede estão ativos.

Execução para teste : python3 ping.py [endereço de rede]
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

def ping_sweep(rede):
	#Recebe um string de rede e retorna uma lista de IPs que responderam ao ping
	hosts_ativos = []

	"""
	ipadress.ip_network() pega o string da rede e transforma em um objeto python inteligente, permitindo extrair informações como máscara de sub rede e IP de broadcast.
	strict=false  permite passar um ip que não seja de início de rede.
	.hosts () gera todos os IPs utilizaveis dessa faixa (sem o de rede e o broadcast)
	"""
	rede_obj = ipaddress.ip_network(rede, strict=False)

	for ip in rede_obj.hosts():
		print(f"Testando {ip}...", end="\r") #vizualização do processo

		if ping_host(ip):
			print(f"Host ativo: {ip}                ")
			hosts_ativos.append(str(ip)) #.append adiciona ao final da lista hosts_ativos o ip (em string) que respondeu ao ping.

	print("                             \n")
	return hosts_ativos

#O código abaixo roda apenas se esse arquivo for executado sozinho
if __name__ == "__main__":
	if len(sys.argv) != 2: #sys.argv guarda os argumentos digitados no terminal em uma lista, separando os itens pelo espaço.
		print("Uso: python3 ping.py [rede]")
		print("Exemplo: python3 ping.py 192.168.1.0/24")
		sys.exit(1) #fecha o programa com o código de erro 1.

	rede_alvo = sys.argv[1] #guarda o segundo argumento digitado (o endereço de rede) na variável.

	print(f"Iniciando ping sweep em {rede_alvo}...\n")
	ativos = ping_sweep(rede_alvo) #chama o método ping_sweep para a rede alvo e guarda a lista de hosts ativos

	print(f"\nTotal de hosts ativos: {len(ativos)}")
	for ip in ativos:
		print(f" - {ip}")
