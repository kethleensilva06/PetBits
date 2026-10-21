## Why

A tela de Pedidos da clínica lista os pedidos, mas não soma nada. Para saber
quanto a loja vendeu num filtro ("Pagos", "Entregues") ou levar os números
para uma planilha, a gerência copia pedido por pedido.

## What Changes

- No alto da lista, um resumo do que está na tela, respeitando o filtro de
  situação e a busca: quantos pedidos e o total, sem os cancelados no total.
- **Baixar CSV**: os pedidos da tela num arquivo para planilha (separado por
  ponto e vírgula, com acentos corretos no Excel): número, data, cliente,
  situação, entrega, pagamento, origem, itens e total. Sem telefone, documento
  nem endereço.
- Montado na tela, sem requisição.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: a equipe vê o total dos pedidos filtrados e os exporta.

## Impact

- Código: `petbits/relatorio.py` (novo), `petbits/states/equipe_state.py`,
  `petbits/pages/equipe.py`; `tests/test_relatorio.py`.
