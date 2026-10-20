## Why

Produto sem estoque some da loja do cliente, e a equipe só descobre quando
alguém pergunta. Nada no sistema avisa que um produto está acabando.

## What Changes

- O painel da clínica ganha **Estoque**: quantos produtos ativos estão
  esgotados e quantos têm 5 unidades ou menos. Clicar abre Produtos já
  filtrado por estoque baixo.
- Produtos ganha o filtro **Todos | Estoque baixo** (ativos com 5 ou menos,
  esgotados primeiro), e o selo do estoque fica vermelho em zero e âmbar até 5.
- As duas contagens entram no próprio `GET equipe/painel`, sem linha: o
  painel continua numa requisição só.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `painel-da-clinica`: o painel mostra os produtos esgotados e acabando.

## Impact

- Backend: `apis/pet_bits/equipe_painel.xs` (duas contagens).
- Código: `petbits/painel.py`, `petbits/states/equipe_state.py`,
  `petbits/pages/equipe.py`; `tests/test_painel.py`.
