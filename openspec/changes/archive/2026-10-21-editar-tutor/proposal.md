## Why

Na clínica, a aba Tutores só lista e cadastra: não dá para corrigir o nome, o
CPF, o telefone, o e-mail ou o endereço de um tutor. Do lado do cliente, o
perfil diz "CPF e e-mail só a clínica altera" — e a clínica não tinha como.

## What Changes

- Na aba Tutores, cada tutor ganha **Editar**: nome, CPF, telefone, e-mail e
  endereço, para toda a equipe (atendente e gerência), como o cadastro de
  balcão.
- Novo endpoint `PATCH equipe/tutores/{tutor_id}`, com a prova de equipe:
  - só os campos enviados mudam;
  - o CPF passa pelas mesmas regras do cadastro (11 dígitos, válido, não usado
    por outro tutor);
  - o e-mail não pode ser de outro tutor nem de outra conta;
  - quando o tutor tem conta no site, mudar o e-mail muda também o e-mail de
    entrada da conta, na mesma transação — o cliente passa a entrar com o
    novo e-mail e a mesma senha;
  - se a conta ligada à ficha não for de cliente, o e-mail não muda por aqui.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `tutores`: a equipe altera os dados de um tutor.

## Impact

- Backend: `apis/pet_bits/equipe_tutor_update.xs` (novo).
- Código: `petbits/xano.py`, `petbits/states/equipe_state.py`,
  `petbits/pages/equipe.py`; testes.
