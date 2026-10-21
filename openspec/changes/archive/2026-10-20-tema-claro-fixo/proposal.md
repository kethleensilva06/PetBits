## Why

Depois de ver o site nos dois modos, a dona do produto preferiu o claro: o
PetBits fica todo branco, sempre, em qualquer aparelho. O modo escuro e o
ícone de sol/lua da `tema-claro-escuro` saem.

## What Changes

- O tema passa a ser sempre claro (`appearance="light"`), qualquer que seja a
  preferência do sistema ou uma escolha guardada antes no navegador.
- O ícone de sol/lua sai do topo das duas áreas e das portas de entrada.
- O fundo da página vira branco liso: sai o degradê verde-água e coral do
  fundo. Cores, marca, cartões, fotos e o banner da casa continuam.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: o tema é sempre claro, com fundo branco.

## Fora do escopo

- Mudar a cor principal, a fonte ou os componentes.

## Impact

- Código: `petbits/visual.py`, `assets/estilo.css`, `petbits/pages/entrar.py`,
  `petbits/pages/equipe.py`.
- Backend e dependências: nenhum impacto.
