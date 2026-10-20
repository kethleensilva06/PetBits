## Why

O site não diz quando a clínica funciona nem como falar com ela. E a agenda
fechava o sábado às 12h, enquanto a clínica funciona de segunda a sábado, das
8h às 18h (pedido da usuária).

## What Changes

- Horário de funcionamento: **segunda a sábado, das 8h às 18h**; domingo
  fechado. O sábado passa a aceitar agendamento até as 18h, na tela
  (`petbits/agenda.py`) e no Xano (`agendamento_create.xs`).
- E-mail de contato **petbitsgroup@gmail.com**, com link para escrever.
- Horário e e-mail aparecem na página inicial pública e no rodapé de todas as
  telas do cliente; o texto do calendário da agenda passa a dizer o horário
  novo.
- Horário e e-mail ficam num lugar só (`petbits/clinica.py`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `agendamentos`: o sábado funciona das 8h às 18h.
- `identidade-visual`: horário e contato à vista.

## Impact

- Backend: `apis/pet_bits/agendamento_create.xs`.
- Código: `petbits/clinica.py` (novo), `petbits/agenda.py`,
  `petbits/visual.py`, `petbits/pages/` (inicial, cliente, agenda);
  `tests/test_clinica.py`.
