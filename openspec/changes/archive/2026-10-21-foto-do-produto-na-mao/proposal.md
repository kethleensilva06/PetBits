## Why

A equipe já pode trocar a foto de um produto (change `foto-do-produto`), mas
só achando o lugar: ela fica dentro de Editar, não existe ao cadastrar ("Depois
de cadastrar, edite o produto para pôr a foto dele") e uma foto enviada não pode
ser removida para voltar à automática.

## What Changes

- No cartão do produto, a miniatura vira botão ("Trocar foto"), que abre a
  edição na foto.
- Na edição, ao lado de Trocar foto, **Remover foto**: o produto volta a usar a
  foto automática (a do próprio produto que acompanha o app, ou a da
  categoria).
- Ao cadastrar um produto, a foto já pode ser escolhida: ela aparece no
  formulário e é enviada logo depois que o produto é salvo.
- Novo endpoint `DELETE equipe/produtos/{produto_id}/foto`, com a prova de
  equipe.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `produtos`: a foto do produto também ao cadastrar e pode ser removida.

## Impact

- Backend: `apis/pet_bits/equipe_produto_foto_remover.xs` (novo).
- Código: `petbits/xano.py`, `petbits/states/equipe_state.py`,
  `petbits/pages/equipe.py`; testes.
