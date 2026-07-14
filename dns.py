"""
Esse módulo ficará responsável por pegar os nomes de domínio dos endereços IP que estão rodando serviços em portas abertas.
Para isso, ele tentará fazer uma consulta DNS reversa para o endereço IP, que geralmente retorna o nome de domínio associado ao endereço IP, caso exista.
Uso para teste: 
python3 dns.py [ip]
"""

import socket #biblioteca que permite abrirmos conexões TCP.
import sys #biblioteca que permite acessar informações e funcionalidades do interpretador python.


def obter_nome_dominio(ip):
    try:
        # Faz uma consulta DNS reversa para o endereço IP
        #gethostbyaddr retorna uma lista com o nome do host, alias e endereços IP associados ao host. O [0] pega apenas o nome do host.
        nome_dominio = socket.gethostbyaddr(ip)[0]
        return nome_dominio
    
    #socket.herror é uma exceção que ocorre quando não é possível resolver o nome do host para o endereço IP fornecido.
    except socket.herror:
        return None


#o código abaixo só será executado se o arquivo for executado diretamente, e não importado como módulo.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 dns.py <ip>")
        print("Exemplo: python3 dns.py 192.168.0.1")
        sys.exit(1)

    ip_alvo = sys.argv[1]
    nome_dominio = obter_nome_dominio(ip_alvo)

    if nome_dominio:
        print(f"Nome de domínio associado ao IP {ip_alvo}: {nome_dominio}")
    else:
        print(f"Não foi possível encontrar o nome de domínio para o IP {ip_alvo}.")