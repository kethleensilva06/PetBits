## Context

`equipe_painel.xs` existe para que o painel custe uma requisição só (o plano
gratuito dá 10 a cada 20 segundos por instância). O comentário do arquivo
avisa que ele tende a virar "endpoint-deus" e que só devolve contagens, para
não pôr documento e contato de clientes numa tela que fica aberta o dia todo.

## Decisions

### D1. Continua numa requisição só

A agenda do dia e as contagens de pedidos entram no próprio
`GET equipe/painel`, e não em duas chamadas a `equipe/agenda` e
`equipe/pedidos`. Três requisições por abertura de painel, que é a tela
inicial da equipe, gastariam um terço da janela; e `equipe/pedidos` traria
todos os pedidos com itens só para contar três situações.

Cada consulta nova paga o próprio custo: a agenda é a pergunta que o painel
existe para responder, e as contagens de pedido são `return = {type:
"count"}`, sem linha.

### D2. O dia vem da tela

`timestamp dia` (meia-noite em São Paulo, em ms UTC), como em `equipe/agenda`.
A tela já calcula esse início com `agenda.inicio_do_dia_ms`; repetir o fuso
no Xano seria uma segunda regra para o mesmo dia.

### D3. Só as linhas que a recepção precisa

A agenda do painel devolve id, início, fim, situação, nome e espécie do
animal, nome do tutor, serviço e profissional. **Sem** telefone, documento
nem endereço do tutor: quem precisa ligar abre a Agenda, que tem o telefone.
Os cancelados ficam de fora (o `where` já filtra), porque o painel responde
"quem vem hoje".

### D4. Pedidos esperando a equipe

Três contagens: `pendente` (aguardando pagamento), `pago` (a separar) e
`pronto_retirada` (esperando o cliente). `enviado` não entra: está com a
entrega, não com a equipe. Clicar num número leva a `/equipe/pedidos` com o
filtro daquela situação já escolhido.

### D5. A formatação é testável sem o Xano

`petbits/painel.py` transforma a resposta em linhas de tela (`agenda_do_dia`)
e em cartões de pedido (`pedidos_esperando`), funções puras testadas em
`tests/test_painel.py`.

## Risks / Trade-offs

- O painel deixa de ser "só números". O comentário do `.xs` é reescrito para
  dizer o que entrou, por quê, e o que continua proibido (contato e documento).
- Um painel aberto o dia todo mostra a agenda da hora em que abriu. O botão
  "Atualizar" recarrega quando a pessoa quiser; não há atualização sozinha.
