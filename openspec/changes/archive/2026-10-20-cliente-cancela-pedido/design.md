## Decisions

### D1. Posse pelo join, sob trava

Como em `agendamento_cancelar.xs`: o pedido é lido com `join` até o tutor e
`where` pela conta do token, com `lock = true`, dentro da transação. Não há
instante em que um pedido alheio esteja numa variável do endpoint, e alheio e
inexistente dão o mesmo 404.

### D2. Só `pendente` e sem pagamento

O cliente cancela enquanto nada aconteceu do lado da clínica. Pedido `pago`
(dinheiro recebido), `pronto_retirada` (separado) ou adiante: recusa, porque
desfazer envolve a clínica (estorno, produto separado). `pago_em` preenchido
também recusa, por segurança, mesmo em `pendente`.

### D3. Estoque devolvido na mesma transação

O mesmo laço do `equipe_pedido_situacao.xs`: cada item volta ao estoque do
produto, lido com trava. Ou o estoque volta e o pedido fica `cancelado`, ou
nada muda.

### D4. Botão só quando o backend aceitaria

`pode_cancelar` na tela é `situacao == pendente` e sem `pago_em`. É
conveniência: quem decide é o endpoint.
