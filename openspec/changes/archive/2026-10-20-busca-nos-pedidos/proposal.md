## Why

A tela de Pedidos da clínica filtra por situação, mas não procura. Quando um
cliente chega no balcão dizendo "vim buscar o pedido 14" ou "o da Ana", a
equipe rola a lista.

## What Changes

- Um campo de busca em Pedidos, como o de Tutores e Animais
  (`busca-na-clinica`): número do pedido, nome ou telefone do cliente, ou nome
  de um produto do pedido. Sem acento nem maiúscula, todas as palavras.
- Vale junto com o filtro de situação, e sem requisição a mais.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: a equipe procura pedidos por número, cliente ou produto.

## Impact

- Código: `petbits/states/equipe_state.py`, `petbits/pages/equipe.py`;
  `tests/test_busca.py`.
