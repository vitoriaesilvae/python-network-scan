"""
Esse módulo receberá os resultados coletados pelos outros módulos e os organizará em um relatório final, que será salvo em /reports.
"""

import json #biblioteca que permite trabalhar com arquivos JSON.
import os #biblioteca que permite trabalhar com o sistema operacional, como criar pastas e arquivos.    
import csv #biblioteca que permite trabalhar com arquivos CSV.

def gerar_relatorio_json(resultados, caminho="reports/resultado.json"):
    """
    Recebe um dicionário de resultados e salva em um arquivo JSON.
    """

    #Cria a pasta reports se não existir
    #Exist_ok=True faz com que não ocorra erro se a pasta já existir.
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    #Abre o arquivo para escrita (w) e salva o dicionário de resultados em formato JSON
    #with open é um gerenciador de contexto que garante que o arquivo será fechado corretamente após a escrita. 
    #"w" significa que o arquivo será aberto para escrita, e se ele não existir, será criado. Se ele já existir, seu conteúdo será sobrescrito.
    #encoding="utf-8" garante que o arquivo será salvo com codificação UTF-8, que suporta caracteres especiais.
    with open(caminho, "w", encoding="utf-8") as arquivo:
        #json.dump converte o dicionário de resultados em uma string JSON e escreve no arquivo.
        #indent=4 faz com que o JSON seja formatado com identação de 4 espaços, facilitando a leitura.
        json.dump(resultados, arquivo, indent=4)

    print(f"Relatório salvo em {caminho}")

def gerar_relatorio_csv(resultados, caminho="reports/resultado.csv"):
    """
    Recebe um dicionário de resultados e salva em um arquivo CSV.
    """

    #Cria a pasta reports se não existir
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    #Abre o arquivo para escrita (w) e salva o dicionário de resultados em formato CSV
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        #Cria um objeto writer que escreve no arquivo CSV
        escritor_csv = csv.writer(arquivo)

        #Escreve o cabeçalho do CSV
        #writerow escreve uma linha no arquivo CSV, e cada elemento da lista será uma célula na linha.
        escritor_csv.writerow(["IP", "Porta", "Serviço", "Banner", "Nome de Domínio"])

        #Escreve os resultados no CSV
        #.items() retorna uma lista de tuplas (chave, valor) do dicionário, permitindo iterar sobre os IPs e suas portas.
        for ip, portas in resultados.items():
            for porta, info in portas.items():
                escritor_csv.writerow([ip, porta, info.get("servico"), info.get("banner"), info.get("nome_dominio")])

    print(f"Relatório salvo em {caminho}")

def gerar_relatorio_html(resultados, caminho="reports/resultado.html"):
    """
    Recebe um dicionário de resultados e salva em um arquivo HTML.
    """

    #Cria a pasta reports se não existir
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    #Abre o arquivo para escrita (w) e salva o dicionário de resultados em formato HTML
    with open(caminho, "w", encoding="utf-8") as arquivo:
        #Escreve o cabeçalho do HTML
        arquivo.write("<html><head><meta charset='UTF-8'><title>Relatório de Scan de Rede</title>")
        arquivo.write("<style>table {border-collapse: collapse;} th, td {border: 1px solid black; padding: 5px;}</style></head><body>")
        arquivo.write("<h1>Relatório de Scan de Rede</h1>")

        #Escreve os resultados no HTML
        for ip, portas in resultados.items():
            arquivo.write(f"<h2>Host: {ip}</h2>")
            arquivo.write("<table><tr><th>Porta</th><th>Serviço</th><th>Banner</th><th>Nome de Domínio</th></tr>")
            
            for porta, info in portas.items():
                arquivo.write(f"<tr><td>{porta}</td><td>{info.get('servico')}</td><td>{info.get('banner')}</td><td>{info.get('nome_dominio')}</td></tr>")
            
            #Fecha a tabela e o HTML
            arquivo.write("</table></body></html>")

    print(f"Relatório salvo em {caminho}")

#O código abaixo só será executado se o arquivo for executado diretamente, e não importado como módulo.
if __name__ == "__main__":
    # Dados de exemplo, simulando o que o scanner.py vai
    # eventualmente montar juntando ping.py + port_scanner.py +
    # banner.py + dns.py + utils.py.
    resultadosEX = {
        "192.168.1.10": {
            22: {"servico": "SSH", "banner": "SSH-2.0-OpenSSH_9.3", "nome_dominio": "pc-vitoria"},
            80: {"servico": "HTTP", "banner": None, "nome_dominio": "pc-vitoria"}
        },
        "192.168.1.1": {
            443: {"servico": "HTTPS", "banner": None, "nome_dominio": None}
        }
    }

    gerar_relatorio_json(resultadosEX)
    gerar_relatorio_csv(resultadosEX)
    gerar_relatorio_html(resultadosEX)