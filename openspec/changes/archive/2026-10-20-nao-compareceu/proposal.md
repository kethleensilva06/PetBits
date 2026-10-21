## Why

Quando o animal não vem, o agendamento fica "Marcado" para sempre: a agenda
da clínica mostra como pendente o que já passou, e o tutor vê um atendimento
que nunca aconteceu como se ainda fosse acontecer. A equipe não tem como
registrar a falta.

## What Changes

- Nova situação de agendamento: **`faltou`** ("Não compareceu").
- Na Agenda da clínica, o agendamento **marcado cujo horário já começou**
  ganha **Não compareceu**, com confirmação.
- Novo endpoint `POST equipe/agendamentos/{agendamento_id}/falta`, com a
  prova de equipe. Só aceita agendamento `marcado` cujo início já passou, pelo
  relógio do Xano.
- Registrar atendimento passa a exigir agendamento `marcado` ou
  `em_andamento`: um agendamento com falta não vira atendimento.
- O tutor vê "Não compareceu" em Meus agendamentos.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `agendamentos`: a equipe registra que o animal não compareceu.

## Impact

- Backend: `tables/agendamento.xs` (valor novo no enum),
  `apis/pet_bits/equipe_agendamento_falta.xs` (novo),
  `apis/pet_bits/equipe_atendimento_create.xs` (precondição).
- Código: `petbits/rotulos.py`, `petbits/xano.py`,
  `petbits/states/equipe_state.py`, `petbits/pages/equipe.py`; testes.
