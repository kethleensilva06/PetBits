## Context

O script da change `ferramentas-de-verificacao` passou 25/25 no Xano de
verdade. As tarefas ainda abertas nas changes `agendamento`, `loja`,
`venda-no-balcao` e `papeis-e-abas` (já arquivada) são, em boa parte, recusas
que ele não exercita.

## Decisions

### D1 — A segunda conta de cliente

O script usa a primeira e a segunda conta de cliente com senha. Com a
segunda: listar agendamentos e pedidos (não vê os da primeira), marcar com o
animal da primeira (recusado) e cancelar o agendamento da primeira (resposta
de inexistente). Sem segunda conta, esses cenários saem como pulados.

### D2 — Recusas com dado que se desfaz

Cada recusa é tentada de forma que, se o backend errar e aceitar, o dado
criado seja reconhecível e desfeito quando possível (pedido cancelado,
produto desativado). O cancelamento com menos de 24 h é pulado: para testá-lo
seria preciso marcar um horário a menos de 24 h, que nenhuma tela nem endpoint
consegue cancelar depois — o teste local `pode_cancelar` e a leitura do
endpoint cobrem a regra.

### D3 — O Xano simulado vira teste

O simulador usado para conferir o script na change anterior era descartável.
Ele vai para `tests/test_ponta_a_ponta.py`, aplicando as regras das specs, e
o teste confere: tudo passa com o backend certo; com a baixa de estoque
quebrada, o script acusa e sai 1.

## Risks / Trade-offs

- [O simulador divergir do Xano] → Ele só existe para testar o script; quem
  confere o Xano é a rodada de verdade.
