## Why

Meus pedidos mistura o que ainda está a caminho com o que já foi entregue ou
cancelado. Com o tempo, o pedido que importa — o que está aguardando
pagamento ou pronto para retirada — fica no meio de compras antigas.

## What Changes

- Meus pedidos em duas partes, como Meus agendamentos
  (`proximos-e-anteriores`):
  - **Em andamento**: aguardando pagamento, pagos, prontos e enviados;
  - **Finalizados**: entregues e cancelados, fechados por padrão atrás de
    "Mostrar finalizados (N)".
- Sem pedido em andamento, a parte de cima diz isso e leva à Loja.
- As duas partes do mais recente para o mais antigo, como hoje.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: Meus pedidos separa os em andamento dos finalizados.

## Impact

- Código: `petbits/etapas_do_pedido.py`, `petbits/states/loja_state.py`,
  `petbits/pages/loja.py`; `tests/test_etapas_do_pedido.py`.
