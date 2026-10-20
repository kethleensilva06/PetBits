## Why

O carrinho da loja mora só na memória do servidor do Reflex. Um F5, uma aba
nova ou o servidor reiniciado esvaziam o carrinho, e o tutor tem de escolher
tudo de novo. A sessão de login, ao contrário, sobrevive a isso, porque fica
no navegador.

## What Changes

- O carrinho passa a ficar no navegador (`rx.LocalStorage`), como a sessão:
  sobrevive ao F5, à aba nova e ao reinício do servidor.
- Ao abrir a loja, o carrinho guardado é conferido com o catálogo que chegou:
  produto que saiu da loja some, e quantidade acima do estoque é reduzida
  (a conferência já existe; passa a valer também para o guardado).
- Sair da conta apaga o carrinho guardado, como apaga o resto.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: o carrinho do cliente sobrevive a recarregar a página.

## Fora do escopo

- Guardar o carrinho no Xano, para ele seguir a conta em outro aparelho.

## Impact

- Código: `petbits/carrinho.py` (novo), `petbits/states/loja_state.py`;
  `tests/test_carrinho.py`.
- Backend: nenhum.
