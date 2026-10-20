## Why

Na clínica, as telas Colaboradores, Tutores e Animais mostram a lista
inteira, sem busca. Quem está no balcão e precisa achar a ficha de um tutor
ou de um animal rola a lista até encontrar — e ela só cresce.

## What Changes

- Um campo de busca no alto de Colaboradores, Tutores e Animais.
- A busca ignora maiúsculas e acentos, aceita várias palavras (todas têm de
  aparecer) e procura em:
  - colaboradores: nome, função, e-mail e telefone;
  - tutores: nome, CPF, telefone e e-mail; CPF e telefone também só pelos
    números ("12345" acha "123.45...");
  - animais: nome, espécie, raça e nome do tutor.
- Sem resultado, a tela diz que nada foi encontrado para aquela busca.
- Filtra a lista que já está na tela: nenhuma requisição a mais.
- Ao trocar de tela, a busca começa vazia.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `acesso-da-equipe`: as listas da clínica têm busca.

## Impact

- Código: `petbits/busca.py` (novo), `petbits/states/equipe_state.py`,
  `petbits/pages/equipe.py`; `tests/test_busca.py`.
- Backend: nenhum.
