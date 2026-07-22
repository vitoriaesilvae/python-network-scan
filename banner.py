"""
Esse módulo ficará responsável pelo Banner Grabbing, ou seja, tentar coletar informações de serviços que estão rodando em portas abertas.
Para isso, ele tentará se conectar a uma porta aberta e ler a resposta do serviço,
que geralmente contém informações sobre o serviço, como versão, sistema operacional, etc.

Uso para teste: 
python3 banner.py [ip] [porta]
"""

import socket #biblioteca que permite abrirmos conexões TCP.
import sys #biblioteca que permite acessar informações e funcionalidades do interpretador python.

"""
Em algumas portas é preciso enviar uma requisição para que o serviço responda com informações sobre ele.
Por exemplo, para HTTP, podemos enviar uma requisição GET e o servidor irá responder com informações
"""
PORTAS_QUE_REQUEREM_REQUISICAO = {80}
# A porta https (443) não é suportada, pois o banner grabbing não funciona com SSL/TLS.

def banner_grabbing(ip, porta, timeout=2):
    """
    Tenta abrir uma conexão TCP com o socket TCP (ip+porta) e ler a resposta do serviço.
    Retorna o banner do serviço, ou None se não conseguir.
    """

    #Cria um objeto socket com ipv4 (AF_INET) e porta tcp (SOCK_STREAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Limita o tempo de espera da resposta a 2 segundos por padrão.
    sock.settimeout(timeout)

    try:
        #Tenta conectar ao serviço
        sock.connect((ip, porta))

        #Se a porta requer uma requisição, envia uma requisição HTTP GET
        if porta in PORTAS_QUE_REQUEREM_REQUISICAO:
            sock.sendall(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            #Essa requisição é um exemplo simples de uma requisição HTTP GET, que solicita a página inicial do servidor.
            #sendall envia todos os bytes da requisição, e o b antes da string indica que é uma string de bytes.

        #Lê até 1024 bytes da resposta do serviço
        #decode transforma os bytes recebidos em string, ignorando erros de decodificação com errors='ignore'.
        banner = sock.recv(1024).decode(errors='ignore')

    #A porta pode estar aberta mas recusar, gerando o erro ConnectionRefusedError, ou o serviço pode não responder a tempo gerando socket.timeout.
    #Uma exceção é um codigo de erro que indica que algo deu errado, e o programa não conseguiu continuar.
    #Os parâmetros de exceção são os tipos de erro que podem ocorrer durante a conexão e leitura do banner.
    #OSError é uma exceção genérica que pode ocorrer em operações de entrada/saída, como leitura e escrita em sockets.
    except (socket.timeout, ConnectionRefusedError,OSError) as e:
        banner = None

    #Finally é um bloco de código que sempre será executado, mesmo que ocorra uma exceção.
    #Ele é usado para garantir que o socket seja fechado ao fim da operação, evitando vazamento de recursos.
    finally:
        sock.close()

    #Retorna em string o banner do serviço, ou None se não conseguiu ler.
    return banner

#O codigo abaixo só será executado se o arquivo for executado diretamente, e não importado como módulo.
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 banner.py <ip> <porta>")
        print("Exemplo: python3 banner.py 192.168.0.1 80")
        sys.exit(1)
    
    ip_alvo = sys.argv[1]
    porta_alvo = int(sys.argv[2])

    print(f"Coletando banner do serviço em {ip_alvo}:{porta_alvo}...\n")
    resultado = banner_grabbing(ip_alvo, porta_alvo)

    if resultado:
        print(f"Banner coletado:\n{resultado}")
    else:
        print("Não foi possível coletar o banner do serviço.")