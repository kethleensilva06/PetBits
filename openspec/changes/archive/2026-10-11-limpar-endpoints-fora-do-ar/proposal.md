## Why

A guarda `verificar_equipe.py` (conferência 5) acusava cinco endpoints
públicos sem motivo escrito: `auth/login`, `auth/signup`,
`message/send_welcome_email`, `reset/magic_link_login` e
`reset/request_reset_link`. Nenhum deles está publicado no Xano — a entrada
do PetBits é `POST entrar` e o cadastro é `POST tutor/cadastro` —, mas os
`.xs` continuavam no repositório. O mesmo vale para `me_tutor_create.xs`
(`POST me/tutor`), da change abandonada `cadastro-de-cliente-pela-conta`.

Arquivo de endpoint fora do ar engana quem lê o repositório e trava as
tarefas de validação de várias changes, que pedem a guarda limpa.

## What Changes

- Saem do repositório os cinco `.xs` de `apis/authentication/` que não estão
  no Xano e `apis/pet_bits/me_tutor_create.xs`.
- `POST me/tutor` é despublicado no painel do Xano, por quem desenvolve (o
  Xano CLI não apaga um endpoint só).
- A spec `publicacao` passa a dizer que o repositório não guarda endpoint
  fora do ar.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `publicacao`: o repositório só guarda endpoints que estão no ar.

## Impact

- `apis/authentication/` fica com `auth/me`, `reset/update_password` e o
  `api_group.xs`; `apis/pet_bits/` perde `me_tutor_create.xs`.
- `verificar_equipe.py` passa sem acusação, o que libera as tarefas de
  validação das changes abertas.
