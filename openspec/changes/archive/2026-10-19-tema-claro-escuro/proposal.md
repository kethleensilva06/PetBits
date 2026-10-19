## Why

Hoje o PetBits fica claro ou escuro conforme o sistema operacional, sem
escolha na tela — a `identidade-visual` deixou o seletor fora do escopo. Quem
usa o computador da recepção à noite, ou prefere o claro num celular em modo
escuro, não tem como trocar.

## What Changes

- Um ícone de sol/lua no topo das duas áreas (cliente e clínica) e no canto
  das portas de entrada alterna entre claro e escuro.
- Sem escolha feita, continua seguindo o sistema. A escolha fica guardada
  neste navegador e vale nas próximas visitas.
- Usa o modo de cor do próprio Reflex (`rx.toggle_color_mode`), que o tema
  (`appearance="inherit"`) já segue: nenhuma cor muda, nenhuma requisição.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: a aparência segue o sistema até a pessoa escolher.

## Fora do escopo

- Guardar a escolha na conta (no Xano), para valer em outro aparelho.
- Uma terceira opção "sistema" no ícone: basta não escolher.

## Impact

- Código: `petbits/visual.py` (o botão), topo do cliente, topo da clínica e
  portas de entrada (`petbits/pages/entrar.py`, `equipe.py`).
- Backend e dependências: nenhum impacto.
