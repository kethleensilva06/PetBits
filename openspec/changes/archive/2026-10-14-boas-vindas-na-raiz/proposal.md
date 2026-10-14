## Why

O endereço principal (`/`) é hoje a área do cliente logado, e quem chega sem
sessão é desviado para `/boas-vindas`. A página de boas-vindas é a porta do
sistema, mas não mora no endereço principal; e a entrada de clientes fica em
`/entrar`, enquanto a da equipe fica em `/entrar/equipe` — as duas portas não
têm a mesma forma.

## What Changes

- **`/` passa a ser a página de boas-vindas.** Quem já entrou e abre `/` é
  levado à sua área, como hoje acontece em `/boas-vindas`.
- **A entrada de clientes ganha página própria em `/entrar/cliente`**,
  espelhando `/entrar/equipe`.
- **A área do cliente logado sai de `/` e vai para `/inicio`.** O destino de
  uma conta de cliente depois da entrada passa a ser `/inicio`.
- **Os endereços antigos continuam funcionando:** `/entrar` leva a
  `/entrar/cliente` e `/boas-vindas` leva a `/`. Um link guardado ou um
  favorito não quebra.
- Os links internos (logo, "Meus animais", "Voltar ao início", "Entrar") e os
  redirecionamentos de sessão passam a apontar para os endereços novos.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: a página inicial pública mora no endereço principal, a
  entrada de clientes tem endereço próprio, e o funcionário que abre a área de
  cliente pelo endereço (`/inicio`) continua sendo levado à gerência.

## Fora do escopo

- Mudar o conteúdo ou o visual das telas de boas-vindas e de entrada.
- Qualquer mudança no backend: a verificação de credencial e a regra de papel
  e página continuam as mesmas.

## Impact

- `petbits/petbits.py` (rotas), `petbits/xano.py` (`ROTA_TUTOR`),
  `petbits/states/auth_state.py`, `sessao.py`, `pet_state.py`,
  `equipe_state.py`, `petbits/pages/entrar.py`, `agenda.py`, `loja.py`.
- Testes de destino por papel e de sessão.
- `README.md` (endereços).
