## Why

Enquanto uma lista não chega, as telas mostram um spinner com "Carregando...".
Quando os dados chegam, os cartões aparecem de uma vez e empurram o resto da
página para baixo. A tela "pula", e a pessoa não sabe o que está vindo.

## What Changes

- Um componente de esqueleto em `petbits/esqueletos.py`: blocos cinza que
  pulsam, no formato do que vai aparecer (cartões em grade, linhas de lista,
  o perfil, os horários).
- O esqueleto substitui o spinner nas cargas de página: casa (animais),
  agenda (meus agendamentos e horários livres), loja (produtos), meus
  pedidos, perfil, histórico, o painel e as listas da clínica.
- Para leitor de tela, o esqueleto continua dizendo "Carregando ...".
- Os spinners dentro de botões (enviando foto, salvando) continuam como estão.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: as cargas de tela mostram esqueletos.

## Fora do escopo

- Mudar quando cada tela carrega ou quantas requisições faz.

## Impact

- Código: `petbits/esqueletos.py` (novo); `petbits/pages/inicio.py`,
  `agenda.py`, `loja.py`, `perfil.py`, `historico.py`, `equipe.py`;
  `tests/test_esqueletos.py`.
