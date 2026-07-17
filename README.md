# Scanner de Rede em Python

No código base temos um gargalo muito grande: o tempo de espera das respostas da rede. Então nessa otimização useremos o multithreading, um processo que envolve várias linhas de exe# Scanner de Rede em Python

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

Esta branch possui o código da branch principal otimizado com threads. Para visualizar o código sequencial e a outra otimização, alterne entre as branches do repositório:

*   **`main`**: Versão base, sequencial e estruturada.
*   **`otimizacao-async`**: Versão otimizada com async.
*   **`otimizacao-threads`** (esta branch): Versão de alta performance que implementa multithreading.

---

## Funcionalidades da Versão Threads

*   **Descoberta de Hosts:** Ping sweep de toda a faixa de rede, com múltiplas threads testando conexões ao mesmo tempo para agilizar os testes.
*   **Varredura de Portas:** Escaneamento das portas TCP mais comuns em cada host, também paralelizado por host.
*   **Banner Grabbing:** Conexão direta com a porta aberta para ler o banner do serviço (útil para identificar versões de softwares rodando).
*   **DNS Reverso:** Tradução dos endereços IP em nomes de domínio legíveis.
*   **Dados Estruturados:** Exportação dos resultados em formato JSON, HTML e CSV.

### Por que threads?

O Python possui o GIL (Global Interpreter Lock), que executa o código em apenas uma thread (linha de execução) por vez. Como esse scanner passa a maior parte do tempo esperando respostas da rede, e não processando código, quando uma thread espera pela resposta de um socket/ping, ela libera o GIL para outra thread trabalhar.

Threads foram aplicadas em dois pontos deste projeto: no ping dos hosts e na varredura de portas, onde existe paralelismo real (a mesma ação sendo executada repetidamente e de forma independente para cada IP/porta).

Cada thread realiza um trabalho independente e devolve um resultado usando `executor.map(função, lista)`, que distribui o trabalho entre as threads e devolve os resultados na mesma ordem da lista de entrada, somente depois que tudo termina — evitando problemas de concorrência sem a necessidade de locks manuais.

Essa otimização funciona bem com tarefas de rede, pois permite esperar várias respostas ao mesmo tempo, mas não traria ganho se o gargalo fosse processamento de CPU.

### Exemplo do retorno estruturado (JSON)

```json
{
    "192.168.1.10": {
        "22": {"servico": "SSH", "banner": "SSH-2.0-OpenSSH_9.3", "nome_dominio": "pc-vitoria"},
        "80": {"servico": "HTTP", "banner": null, "nome_dominio": "pc-vitoria"}
    }
}
```