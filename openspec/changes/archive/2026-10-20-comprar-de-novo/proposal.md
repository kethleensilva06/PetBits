## Why

Ração, sachê e areia se compram de novo todo mês. Em Meus pedidos, para
repetir uma compra, o tutor tem de abrir a loja e achar cada produto outra vez.

## What Changes

- Cada pedido em Meus pedidos ganha **Comprar de novo**: os itens dele vão
  para o carrinho, somados ao que já estiver lá, e a tela vai para a Loja.
- Ao abrir a loja, o carrinho é conferido com o catálogo (como já é hoje).
  Se algum item saiu da loja ou teve a quantidade reduzida pelo estoque, o
  carrinho avisa.
- `GET pedido` passa a devolver o `id_produto` de cada item. O filtro pela
  conta do token não muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: repetir um pedido pelo Meus pedidos.

## Impact

- Backend: `apis/pet_bits/pedido_list.xs` (um campo a mais na saída dos itens).
- Código: `petbits/carrinho.py`, `petbits/states/loja_state.py`,
  `petbits/pages/loja.py`; `tests/test_carrinho.py`.
