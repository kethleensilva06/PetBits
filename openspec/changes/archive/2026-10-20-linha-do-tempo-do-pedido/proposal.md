## Why

Em Meus pedidos, cada pedido mostra só um selo com a situação ("Pago",
"Enviado"). O cliente não vê o que já aconteceu nem o que falta, e precisa
saber de cor o caminho do pedido.

## What Changes

- Cada pedido mostra as etapas do seu caminho, com as feitas marcadas e a
  atual destacada:
  - retirada na clínica: Pedido recebido → Pagamento → Pronto para retirada → Retirado;
  - entrega no endereço: Pedido recebido → Pagamento → Enviado → Entregue.
- A etapa do pagamento segue o `pago_em`, e não a situação: na retirada com
  pagamento na loja, o pedido pode ficar pronto antes de pago, e a etapa diz
  "Pagar na retirada".
- O pedido cancelado não mostra etapas: mostra que foi cancelado e que os
  itens voltaram ao estoque.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: Meus pedidos mostra as etapas do pedido.

## Fora do escopo

- Data e hora de cada etapa (o pedido só guarda `created_at` e `pago_em`;
  guardar as outras pediria um histórico de situações no backend).
- Mudanças na tela de pedidos da equipe.

## Impact

- Código: `petbits/etapas_do_pedido.py` (novo), `petbits/states/loja_state.py`,
  `petbits/pages/loja.py`; `tests/test_etapas_do_pedido.py`.
- Backend: nenhum. `GET pedido` já devolve `situacao`, `entrega` e `pago_em`.
