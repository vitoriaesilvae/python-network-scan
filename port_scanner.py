"""
Scanner de portas
Objetivo: Verificar quais portas TCP (de uma lista) estão abertas

Execução de teste:
python3 port_scanner.py [ip] [portas separadas por vírgulas], ou só com o ip.
"""
import socket #biblioteca que permite abrirmos conexões TCP.
import sys #biblioteca que permite acessar informações e funcionalidades do interpretador python.

#Lista padrão de portas comuns
PORTAS_COMUNS = [21,22,23,25,53,80,110,139,143,443,445,3389,8080]

def scan_port(ip, porta, timeout=1):
	"""
	Tenta abrir uma conexão TCP com o socket TCP (ip+porta)
	Retorna true se a porta está aberta, false se não.
	"""

	#Cria um objeto socket com ipv4 (AF_INET) e porta tcp (SOCK_STREAM)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#Limita o tempo de espera da resposta a 1 segundo.
	sock.settimeout(timeout)

	#O .connect_ex tenta conectar e devolve um código de erro, ao invés de gerar uma exceção.
	#Retorna 0 se a porta estiver aberta.
	resultado = sock.connect_ex((ip,porta))

	#Fecha a conexão
	sock.close()

	#Retorna true se o resultado for 0 (porta aberta), false caso contrário.
	return resultado == 0

def scan_host(ip, portas=None, timeout=1):
	"""
	Varre uma lista de portas em um host e devolve a lista das portas abertas.
	"""

	if portas is None:
		portas = PORTAS_COMUNS

	portas_abertas = []

	print(f"Host: {ip}")

	#Verifica a conexão com cada porta da lista, chamando o método acima scan_port.
	for porta in portas:
		if scan_port(ip, porta, timeout):
			print(f"{porta} ABERTA")
			portas_abertas.append(porta)

	print("\n")

	return portas_abertas

#Código para quando o arquivo é executado sozinho:
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Uso: python3 port_scanner.py <ip> [portas separadas por vírgula]")
		print("Exemplo: python3 port_scanner.py 192.168.1.10")
		print("Exemplo: python3 port_scanner.py 192.168.1.10 22,80,443")
		sys.exit(1)

	ip_alvo = sys.argv[1]

	#Se o usuário colocou uma lista de portas customizadas, transforma a string em uma lista de inteiros.
	if len(sys.argv) == 3:
		portas_alvo = [int(x) for x in sys.argv[2].split(",")]
	else:
		portas_alvo = PORTAS_COMUNS

	abertas = scan_host(ip_alvo, portas_alvo)

	print(f"Total de portas abertas: {len(abertas)}")
