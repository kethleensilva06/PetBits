## Why

Ao entrar na Loja, a página fica mais larga que as outras abas da área do
cliente: o conteúdo ocupava 1053 px na Loja e 880 px em Meus animais, Agendar,
Meus pedidos e Meu perfil (medido numa tela de 1100 px). O cabeçalho e o menu
"pulam" a cada troca de aba. A Loja usava a largura 4 do container e as
outras a 3.

## What Changes

- Todas as abas da área do cliente usam a mesma largura, numa constante só
  (`LARGURA_DO_CLIENTE` em `petbits/visual.py`).
- A Loja passa da largura 4 para a 3, como as outras; a Agenda, que não
  declarava largura, passa a declarar a mesma.
- Um teste confere que toda página do cliente usa a constante.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: as abas do cliente têm a mesma largura.

## Fora do escopo

- Mudar a largura da área da clínica (que tem uma só, na casca).
- Redesenhar a grade da loja.

## Impact

- Código: `petbits/visual.py`, `petbits/pages/inicio.py`, `loja.py`,
  `agenda.py`, `perfil.py`; `tests/test_largura.py`.
