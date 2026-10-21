## Why

Na loja, os valores ficavam bagunçados ao escolher os produtos (relato da
usuária). Medido a 1280 px:

- no carrinho, cada item era uma linha só — nome, menos, quantidade, mais e
  total — numa coluna de 272 px: o nome quebrava em duas ou três linhas e o
  valor era cortado ("R$ 39,9");
- os cartões tinham alturas diferentes conforme o tamanho do nome e da
  descrição (374 e 394 px), e o preço ficava em alturas diferentes;
- o estoque aparecia como "28 disponível(is)" ao lado do preço.

## What Changes

- Cada item do carrinho em duas linhas: o nome inteiro com o total da linha,
  e embaixo o preço de cada um com a quantidade.
- Nos cartões, nome e descrição em até duas linhas, com o espaço de duas
  reservado: todo cartão tem a mesma altura e o preço fica no mesmo lugar.
- O preço em destaque com a unidade ao lado ("R$ 24,90 / pacote 4 kg") e o
  estoque embaixo ("28 em estoque").

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `produtos`: cartões e carrinho da loja organizados.

## Impact

- Código: `petbits/pages/loja.py`, `petbits/states/loja_state.py`,
  `assets/estilo.css`.
