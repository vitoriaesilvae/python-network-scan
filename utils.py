"""
Esse módulo contém funções utilitárias que podem ser usadas em outros módulos do projeto.
Contém o dicionário de portas conhecidas, que mapeia números de portas para os serviços que geralmente rodam nessas portas.
Também contém a função que traz o nome do serviço associado a uma porta.
"""

#Dicionário: chave = número da porta, valor = nome do serviço
SERVIÇOS = {
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "Microsoft-DS",
    3389: "Microsoft RDP"
}

def obter_servico(porta):
    #Retorna o nome do serviço associado a uma porta, ou "Desconhecido" se a porta não estiver no dicionário.
    return SERVIÇOS.get(porta, "Desconhecido")

if __name__ == "__main__":
    #Exemplo de uso da função obter_servico
    porta = 80
    print(f"A porta {porta} geralmente roda o serviço: {obter_servico(porta)}")