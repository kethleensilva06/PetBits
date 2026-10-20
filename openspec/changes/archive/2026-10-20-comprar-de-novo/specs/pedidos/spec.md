## ADDED Requirements

### Requirement: Comprar de novo

Cada pedido em Meus pedidos SHALL oferecer Comprar de novo, que põe os itens
do pedido no carrinho, somados ao que já está nele, e leva à loja. Ao abrir a
loja, item fora da loja ou sem estoque SHALL sair do carrinho e quantidade
acima do estoque SHALL ser reduzida, e o carrinho SHALL avisar o que foi
ajustado.

#### Scenario: Repetir um pedido

- **WHEN** a tutora clica em Comprar de novo num pedido com 2 sachês e 1 areia
- **THEN** vai para a loja com 2 sachês e 1 areia no carrinho

#### Scenario: Produto sem estoque

- **WHEN** um dos produtos do pedido está sem estoque
- **THEN** ele não entra no carrinho, e o carrinho avisa que um item saiu
