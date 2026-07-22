# Scanner de Rede em Python

Um scanner de rede simples e estruturado desenvolvido em Python para identificar hosts ativos na rede, escanear portas abertas, capturar banners de serviços ativos e resolver nomes de domínio (DNS).

Este projeto foi construído focado em demonstrar a evolução de arquitetura de código, otimização de performance e boas práticas de controle de versão utilizando Git.

O código foi inteiramente escrito utilizando Linux, então o comando ping está adaptado para este sistema operacional.
Para utilizar em Windows será necessário alterar a escrita do comando de rede ping.

Uso:
python3 scanner.py (seu ip)

Exemplo:
python3 scanner.py 192.168.1.1/24
---

## ⚠️ Aviso Legal

Esta ferramenta foi desenvolvida para fins educacionais. Utilize-a
apenas em redes próprias ou com autorização explícita do responsável
pela rede. Escanear redes de terceiros sem permissão pode configurar
crime, conforme a legislação local.

---

## Estrutura das Branches

A branch principal contém a versão inicial, sequencial e didática do scanner. Para visualizar as implementações focadas em performance e concorrência, alterne entre as branches do repositório:

*   **`main`**: Versão base, sequencial e estruturada.
*   **`otimizacao-async`** (Esta branch): Versão otimizada com `asyncio`, usando um único event loop e corrotinas em vez de threads.
*   **`otimizacao-threads`**: Versão de alta performance que implementa multithreading.

---

## Funcionalidades da Versão Assíncrona

*   **Descoberta de Hosts:** Ping sweep de toda a faixa de rede executado de forma concorrente, com `asyncio.gather` e `asyncio.Semaphore` limitando quantos pings estão "em voo" ao mesmo tempo.
*   **Varredura de Portas:** Escaneamento das portas TCP mais comuns em cada host, também concorrente por host, usando `asyncio.open_connection`.
*   **Banner Grabbing:** Conexão assíncrona com cada porta aberta para ler o banner do serviço (útil para identificar versões de softwares rodando).
*   **DNS Reverso:** Tradução dos endereços IP em nomes de domínio legíveis. Como `socket.gethostbyaddr` é bloqueante, essa chamada roda em uma thread auxiliar via `loop.run_in_executor`, sem travar o event loop principal.
*   **Dados Estruturados:** Exportação dos resultados em formato JSON, HTML e CSV.

### Por que asyncio em vez de threads?

Diferente da branch `otimizacao-threads`, aqui a concorrência acontece dentro de uma única thread. Cada tarefa (pingar um host, escanear uma porta, capturar um banner) é uma corrotina que cede o controle voluntariamente sempre que espera uma resposta de rede (`await`), permitindo que o event loop cuide de outras tarefas nesse meio tempo. Isso reduz o custo de memória por conexão em comparação a threads, o que se torna mais perceptível em faixas de rede grandes.

### Exemplo do retorno estruturado (JSON)

```json
{
    "hosts": [
        {
            "host": "192.168.1.10",
            "hostname": "pc-vitoria",
            "portas": [
                {"porta": 22, "servico": "SSH", "banner": "SSH-2.0-OpenSSH_9.3"},
                {"porta": 80, "servico": "HTTP", "banner": null}
            ]
        },
        {
            "host": "192.168.1.1",
            "hostname": null,
            "portas": [
                {"porta": 443, "servico": "HTTPS", "banner": null}
            ]
        }
    ]
}
```
