## Why

Quem fez um pedido por engano, ou mudou de ideia antes de pagar, não tem como
desfazer: só a clínica cancela. O pedido fica em "Aguardando pagamento",
segurando estoque, até alguém da equipe notar.

## What Changes

- Em Meus pedidos, o pedido **aguardando pagamento** ganha **Cancelar
  pedido**, com confirmação.
- Novo endpoint `POST pedido/{pedido_id}/cancelar`, só do dono do pedido e só
  enquanto ele está `pendente` e sem pagamento registrado. Cancelar devolve o
  estoque de cada item na mesma transação, como o cancelamento da equipe.
- Pedido de outra pessoa e pedido inexistente respondem igual ("não
  encontrado"). Pedido pago, pronto, enviado ou entregue: recusa, e o tutor
  fala com a clínica.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: o cliente cancela o próprio pedido enquanto ele aguarda pagamento.

## Impact

- Backend: `apis/pet_bits/pedido_cancelar.xs` (novo).
- Código: `petbits/xano.py`, `petbits/states/loja_state.py`,
  `petbits/pages/loja.py`; testes.
