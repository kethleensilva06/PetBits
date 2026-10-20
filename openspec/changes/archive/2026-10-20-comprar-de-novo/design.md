## Decisions

### D1. Somar, não substituir

O carrinho pode já ter coisas. `carrinho.somar(atual, itens)` soma as
quantidades do pedido às do carrinho, até o máximo de 99 por produto que o
carrinho guardado aceita.

### D2. A loja confere, a tela avisa

O pedido pode ser antigo: produto inativo, sem estoque ou com menos estoque.
Quem confere é o `carregar_loja`, que já reduz o carrinho ao estoque. Ele
passa a contar o que ajustou e grava um aviso ("1 item saiu do carrinho: sem
estoque ou fora da loja"; "a quantidade de 1 item foi reduzida ao estoque"),
mostrado no carrinho até a próxima mudança nele.

### D3. Só o `id_produto` a mais

`pedido_list.xs` ganha `id_produto` na saída dos itens. É dado do próprio
pedido do tutor; a consulta continua nascendo filtrada pela conta do token.
Item sem `id_produto` (0, de dado antigo) é ignorado ao repetir.
