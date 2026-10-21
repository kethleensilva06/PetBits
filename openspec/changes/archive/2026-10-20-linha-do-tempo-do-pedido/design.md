## Context

O caminho do pedido está em `equipe_pedido_situacao.xs`: `pendente` vai a
`pago`, `pronto_retirada` (retirada) ou `enviado` (endereço); `pago` vai aos
dois últimos; os dois vão a `entregue`; quase tudo pode ir a `cancelado`.
`pago_em` é gravado ao passar a `pago` ou a `entregue`.

## Decisions

### D1. Quatro etapas fixas por tipo de entrega

Recebido, Pagamento, Pronto para retirada/Enviado, Retirado/Entregue. O tipo
de entrega escolhe os rótulos das duas últimas.

### D2. Pagamento pelo `pago_em`

`pendente → pronto_retirada` pula o `pago`: quem paga na loja paga ao
retirar. Se a etapa seguisse a situação, um pedido pronto apareceria como
pago. Ela fica feita só com `pago_em`; sem ele, o rótulo é "Pagar na
retirada" (pagamento na loja) ou "Aguardando pagamento" (online).

### D3. A etapa atual é a seguinte à última feita

Com o pagamento podendo ficar para trás, "a primeira não feita" apontaria
para o pagamento num pedido já pronto. A atual é a seguinte à última feita;
uma etapa não feita antes dela aparece como pendente, sem destaque. Pedido
entregue não tem etapa atual.

### D4. Função pura

`petbits/etapas_do_pedido.py` calcula a lista a partir de `situacao`,
`entrega`, `forma_pagamento` e `pago_em`, testada sem o Xano. O cancelado
devolve lista vazia, e a tela mostra o aviso no lugar.
