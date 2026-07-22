"""
Esse módulo contém funções utilitárias que podem ser usadas em outros módulos do projeto.
Contém o dicionário de portas conhecidas, que mapeia números de portas para os serviços que geralmente rodam nessas portas.
Também contém a função que traz o nome do serviço associado a uma porta.
"""

import socket

def obter_servico(porta):
    #Retorna o nome do serviço associado a uma porta, ou "Desconhecido" se a porta não estiver no dicionário.
    try:
        nome = socket.getservbyport(porta)
        return nome
    except OSError:
        return "Desconhecido"

if __name__ == "__main__":
    #Exemplo de uso da função obter_servico
    porta = 80
    print(f"A porta {porta} geralmente roda o serviço: {obter_servico(porta)}")