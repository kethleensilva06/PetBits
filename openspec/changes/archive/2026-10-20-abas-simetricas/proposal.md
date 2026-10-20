## Why

A change `mesma-largura-no-cliente` deixou as cinco abas do cliente com 880 px,
mas Meus animais e Meus pedidos ainda pareciam de outro tamanho. Medido numa
tela de 1280 px: nessas duas abas, curtas, não há barra de rolagem; o
conteúdo centraliza numa área 8 px maior e começa em 200 px, contra 192 px
nas outras. O cabeçalho, o avatar e o menu "andam" ao trocar de aba.

## What Changes

- O lugar da barra de rolagem fica sempre reservado
  (`scrollbar-gutter: stable` no `html`, em `assets/estilo.css`). Toda aba
  começa no mesmo ponto, com ou sem rolagem.
- Um teste confere a regra na folha de estilo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: as abas ficam no mesmo lugar, e não só com a mesma largura.

## Impact

- Código: `assets/estilo.css`; `tests/test_largura.py`.
