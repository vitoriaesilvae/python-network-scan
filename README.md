# Scanner de Rede em Python

Um scanner de rede simples e estruturado desenvolvido em Python para identificar hosts ativos na rede, escanear portas abertas, capturar banners de serviços ativos e resolver nomes de domínio (DNS).

Este projeto foi construído focado em demonstrar a evolução de arquitetura de código, otimização de performance e boas práticas de controle de versão utilizando Git.

---

## ⚠️ Aviso Legal

Esta ferramenta foi desenvolvida para fins educacionais. Utilize-a
apenas em redes próprias ou com autorização explícita do responsável
pela rede. Escanear redes de terceiros sem permissão pode configurar
crime, conforme a legislação local.

---

## Estrutura das Branches 

A branch principal contém a versão inicial, sequencial e didática do scanner. Para visualizar as implementações focadas em performance e concorrência, alterne entre as branches do repositório:

*   **`main`** (Esta branch): Versão base, sequencial e estruturada.
*   **`otimizacao-async`**: Versão otimizada com async.
*   **`otimizacao-threads`**: Versão de alta performance que implementa multithreading.

---

## Funcionalidades da Versão Base

*   **Descoberta de Hosts:** Identificação de IPs ativos no segmento de rede.
*   **Varredura de Portas:** Escaneamento sequencial das portas TCP mais comuns em cada host.
*   **Banner Grabbing:** Conexão direta com a porta aberta para ler o banner do serviço (útil para identificar versões de softwares rodando).
*   **DNS Reverso:** Tradução dos endereços IP em nomes de domínio legíveis.
*   **Dados Estruturados:** Exportação dos resultados em formato JSON, HTML e CSV.

Exemplo do retorno estruturado json:
```json
{
  "192.168.1.10": {
    "22": {"servico": "SSH", "banner": "SSH-2.0-OpenSSH_9.3", "nome_dominio": "pc-vitoria"},
    "80": {"servico": "HTTP", "banner": null, "nome_dominio": "pc-vitoria"}
  }
}