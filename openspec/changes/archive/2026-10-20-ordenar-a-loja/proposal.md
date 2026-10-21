## Why

A loja tem busca e filtro por categoria, mas os produtos vêm sempre na ordem
do catálogo. Quem quer o mais barato, ou procura pelo nome numa lista longa,
tem de olhar tudo.

## What Changes

- Uma lista **Ordenar** ao lado do filtro de categoria: Em destaque (a ordem
  do catálogo, como hoje), Menor preço, Maior preço e Nome (A–Z).
- A ordem vale junto com a busca e a categoria, e "Limpar a busca" volta a
  Em destaque.
- Na própria tela, sem requisição.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `produtos`: a loja do cliente pode ser ordenada por preço e nome.

## Impact

- Código: `petbits/states/loja_state.py`, `petbits/pages/loja.py`;
  `tests/test_mascaras.py` (onde já ficam os testes do filtro da loja).
