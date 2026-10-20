## ADDED Requirements

### Requirement: Loja organizada

Todo cartão de produto da loja SHALL ter a mesma altura, com o preço no mesmo
lugar, e nome e descrição em até duas linhas. Cada item do carrinho SHALL
mostrar o nome inteiro, o total da linha, o preço de cada um e a quantidade,
sem cortar nenhum valor.

#### Scenario: Cartões lado a lado

- **WHEN** a loja mostra produtos com nomes e descrições de tamanhos diferentes
- **THEN** os cartões têm a mesma altura e o preço aparece na mesma posição em todos

#### Scenario: Carrinho com nome longo

- **WHEN** a tutora põe "Coleira ajustável média" no carrinho
- **THEN** o nome aparece inteiro, e o total e o preço de cada um aparecem sem corte
