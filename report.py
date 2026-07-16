"""
Esse módulo receberá os resultados coletados pelos outros módulos e os organizará em um relatório final, que será salvo em /reports.
"""

import json
import os #biblioteca para manipulação de arquivos e diretórios
import csv

def gerar_relatorio_json(resultados, caminho="reports/resultado.json"):
    """
    Recebe o dicionário {"hosts": [...]} e salva em um arquivo JSON.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
 
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, indent=4, ensure_ascii=False)
 
    print(f"Relatório salvo em {caminho}")
 
 
def gerar_relatorio_csv(resultados, caminho="reports/resultado.csv"):
    """
    Recebe o dicionário {"hosts": [...]} e salva em um arquivo CSV,
    uma linha por porta encontrada.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
 
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(["IP", "HOSTNAME", "PORTA", "SERVICO", "BANNER"])
 
        # resultados["hosts"] é uma LISTA de hosts -> iteração direta, sem .items()
        for host_info in resultados["hosts"]:
            ip = host_info["host"]
            hostname = host_info["hostname"] or "-"
 
            # host_info["portas"] também é uma LISTA (de dicionários),
            for porta_info in host_info["portas"]:
                escritor_csv.writerow([
                    ip,
                    hostname,
                    porta_info["porta"],
                    porta_info["servico"],
                    porta_info.get("banner") or "-",
                ])
 
    print(f"Relatório salvo em {caminho}")
 
 
def gerar_relatorio_html(resultados, caminho="reports/resultado.html"):
    """
    Recebe o dicionário {"hosts": [...]} e salva em um arquivo HTML,
    uma tabela por host.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
 
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("<html><head><meta charset='UTF-8'><title>Relatório de Scan de Rede</title>")
        arquivo.write("<style>table {border-collapse: collapse;} th, td {border: 1px solid black; padding: 5px;}</style></head><body>")
        arquivo.write("<h1>Relatório de Scan de Rede</h1>")
 
        for host_info in resultados["hosts"]:
            ip = host_info["host"]
            hostname = host_info["hostname"] or "-"
 
            arquivo.write(f"<h2>Host: {ip} ({hostname})</h2>")
            arquivo.write("<table><tr><th>Porta</th><th>Serviço</th><th>Banner</th></tr>")
 
            for porta_info in host_info["portas"]:
                porta = porta_info["porta"]
                servico = porta_info["servico"]
                banner = porta_info.get("banner") or "-"
                arquivo.write(f"<tr><td>{porta}</td><td>{servico}</td><td>{banner}</td></tr>")
 

            arquivo.write("</table>")
 
        arquivo.write("</body></html>")
 
    print(f"Relatório salvo em {caminho}")
 
 
if __name__ == "__main__":
    # Dados de exemplo no MESMO formato que scanner.py produz de verdade.
    resultadosEX = {
        "hosts": [
            {
                "host": "192.168.1.10",
                "hostname": "pc-vitoria",
                "portas": [
                    {"porta": 22, "servico": "SSH", "banner": "SSH-2.0-OpenSSH_9.3"},
                    {"porta": 80, "servico": "HTTP", "banner": None},
                ],
            },
            {
                "host": "192.168.1.1",
                "hostname": None,
                "portas": [
                    {"porta": 443, "servico": "HTTPS", "banner": None},
                ],
            },
        ]
    }
 
    gerar_relatorio_json(resultadosEX)
    gerar_relatorio_csv(resultadosEX)
    gerar_relatorio_html(resultadosEX)
