## Why

A clínica também vende no balcão: o cliente escolhe o produto na loja física,
paga ali e leva. Essa venda precisa baixar o estoque como a do site e ficar
registrada na conta do cliente, para aparecer em "Meus pedidos". É a última
das três changes da loja.

## What Changes

- **Venda no balcão** (`/equipe/balcao`): o atendente escolhe o cliente,
  monta a venda com os produtos à venda e confirma. A venda nasce
  **entregue e paga**, com pagamento na loja, e fica na conta do cliente.
- **Origem do pedido:** `pedido` ganha a coluna `origem` (`site` ou
  `balcao`), para a clínica distinguir as vendas. Pedidos antigos ficam como
  `site`.
- **Uma regra de estoque só:** a lógica de baixar estoque com trava,
  congelar preço e somar o total sai do `POST pedidos` para a função
  `PetBits/registrar_pedido`, usada pelo site e pelo balcão. O `POST pedidos`
  é republicado chamando a função, sem mudar o que faz.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: venda presencial registrada pela equipe na conta do cliente.

## Fora do escopo

- Cliente sem cadastro (venda avulsa): a venda é sempre na conta de um
  cliente cadastrado.
- Troco, cupom fiscal, formas de pagamento no balcão.

## Impact

- Xano: coluna `pedido.origem`; função `PetBits/registrar_pedido`; endpoint
  novo `POST equipe/vendas`; `POST pedidos` republicado usando a função.
- Reflex: `/equipe/balcao` e o item no menu da equipe; "Meus pedidos" e os
  pedidos da equipe mostram a origem.
