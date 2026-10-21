## ADDED Requirements

### Requirement: O painel avisa o estoque baixo

O painel da clínica SHALL mostrar quantos produtos ativos estão esgotados e
quantos têm 5 unidades ou menos, sem requisição a mais. Clicar SHALL abrir
Produtos filtrado por estoque baixo, com os esgotados primeiro. Produto
inativo MUST NOT contar.

#### Scenario: Produto acabando

- **WHEN** um produto ativo tem 3 unidades
- **THEN** o painel conta 1 produto acabando, e Produtos com Estoque baixo mostra esse produto

#### Scenario: Produto inativo

- **WHEN** um produto inativo tem 0 unidades
- **THEN** ele não entra na contagem de esgotados
