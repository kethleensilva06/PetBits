## Why

Um endereço que não existe (link velho, erro de digitação) mostra a página
padrão do Reflex: "404: Page not found", em inglês, numa tela branca, sem a
marca e sem caminho de volta.

## What Changes

- Uma página "não encontrada" com a cara do PetBits: a marca, uma foto que
  já acompanha o app (o coelho, `outro.webp`), o título "Página não
  encontrada", uma frase e dois botões: **Ir ao início** e **Voltar**.
- O título da aba passa a "PetBits | Página não encontrada".
- Nenhuma requisição ao Xano.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: endereço inexistente mostra a página não encontrada do PetBits.

## Impact

- Código: `petbits/pages/nao_encontrada.py` (novo), `petbits/petbits.py`;
  `tests/test_nao_encontrada.py`.
