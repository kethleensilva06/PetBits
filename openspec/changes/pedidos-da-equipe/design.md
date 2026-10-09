## Context

`pedido` e `pedido_item` nasceram na change `loja`, com as seis situações já
no enum. Padrões: abertura de equipe com `exige_equipe` (guarda
`verificar_equipe.py`), transação com trava, só operadores já executados pelo
motor (`>`, `==`, `!=`, `||`, `&&`).

## Decisions

### D1 — Leitura em duas consultas

`GET equipe/pedidos?situacao=` devolve os pedidos (com `join` até `tutor` para
nome e telefone) e, numa segunda consulta, os itens desses pedidos. Filtro
vazio traz todos. O Python agrupa, como em "Meus pedidos".

### D2 — Transições conferidas no servidor, por tabela explícita

`POST equipe/pedidos/{id}/situacao` recebe só a situação nova. O endpoint lê o
pedido **com trava** dentro de uma transação e confere a transição por uma
sequência de condições por igualdade — a regra da change
`operacao-da-clinica` para papel vale aqui para situação: nunca "qualquer
coisa diferente de". Transição fora da tabela → recusa, sem gravar.

### D3 — Pagamento por data, não por situação

A situação é uma só, e `pago` deixa de aparecer quando o pedido avança. Quem
diz se foi pago é `pago_em`: gravado ao ir para `pago`, ou ao ir para
`entregue` sem `pago_em` (pagamento na retirada ou na entrega). Nunca é
sobrescrito.

### D4 — Cancelar devolve estoque na mesma transação

Ao cancelar, para cada item: lê o produto com trava e soma a quantidade ao
estoque. Tudo dentro da transação da mudança de situação: o rollback (medido
na change `acesso-do-tutor`) desfaz tudo se algo falhar.

## Risks / Trade-offs

- [Pedido online já pago cancelado] → O pagamento é simulado; não há estorno
  a fazer. Fica registrado `pago_em` e a situação `cancelado`.
