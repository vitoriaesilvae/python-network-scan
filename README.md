# Scanner de Rede em Python

No código base temos um gargalo muito grande: o tempo de espera das respostas da rede. Então nessa otimização useremos o multithreading, um processo que envolve várias linhas de execução trabalhando ao mesmo tempo para agilizar os testes de conexão.

O python possui o GIL (Global Interpreter Lock)que executa o código em apenas uma thread (linha de execução) por vez. Como esse scanner passa maior parte do tempo esperando respostas da rede e não processando o código, quando uma thread espera pela responsta de socket/ping, ela libera o GIL para outra thread trabalhar.

O threads foi aplicado em dois pontos desse projeto, no ping dos hosts e no scan de portas, onde existem paralelismos (mesma ação sendo executada repetidamente e separadamente).

Cada thread faz um trabalho independente e devolve um resultado usando executor.map(função,lista), que distribui o trabalho entre as threds e devolve os resultados na mesma ordem da lista de entrada depois de tudo terminar.

Essa otimização funciona bem com tarefas de redes pois consegue esperar várias coisas ao mesmo tempo, mas não ajudaria se o gargalo fosse o processamento da CPU.

---

## Estrutura das Branches 

Esta branch possui o código da branch principal otimizado com threads. Para visualizar o código sequencial e a outra otimização, alterne entre as branches do repositório:

*   **`main`** : Versão base, sequencial e estruturada.
*   **`otimizacao-async`**: Versão otimizada com async.
*   **`otimizacao-threads`** (esta branch): Versão de alta performance que implementa multithreading.

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