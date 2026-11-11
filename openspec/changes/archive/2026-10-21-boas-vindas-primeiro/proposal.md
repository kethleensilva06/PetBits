## Why

O endereço principal (`/`) é a casa do cliente. Para quem chega sem sessão, o
site publicado entrega primeiro essa casa ("Olá, … Meus animais", medido no
HTML de `/` no Reflex Cloud e no GitHub Pages) e só depois que o servidor
conecta leva à página de boas-vindas. O visitante vê a tela de cliente piscar
antes da vitrine. A usuária quer a boas-vindas em primeiro lugar.

## What Changes

- `/` passa a ser a página de boas-vindas. `/boas-vindas` continua, para
  links antigos.
- A casa do cliente (Meus animais) muda para `/animais`: o menu, a marca da
  área do cliente, a entrada e os redirecionamentos de sessão passam a levar
  para lá.
- Quem já entrou e abre `/` continua indo direto para a sua área.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: o endereço principal é a página inicial pública.
- `identidade-visual`: a marca da área do cliente leva a `/animais`.

## Impact

- Código: `petbits/petbits.py`, `petbits/xano.py`, `petbits/visual.py`,
  `petbits/pages/` (início, entrar, agenda), `petbits/states/` (sessão);
  testes.
