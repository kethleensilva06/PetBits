## Why

A casa do cliente (Meus animais) não diz nada sobre o que vem pela frente.
Para lembrar quando é a consulta da Mel, o tutor tem de abrir Agendar e
procurar na lista.

## What Changes

- Logo abaixo do banner, um cartão **Próximo agendamento**: serviço e animal,
  dia ("hoje", "amanhã" ou o dia por extenso) e hora, o profissional, e o
  atalho Ver na agenda. Se houver mais de um, diz quantos outros há.
- Sem agendamento futuro, o cartão diz isso e oferece Agendar.
- Uma requisição a mais ao abrir a casa (`GET agendamentos`). Se ela falhar,
  a casa continua normal, só sem o cartão.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `agendamentos`: a casa do cliente mostra o próximo agendamento.

## Impact

- Código: `petbits/proximo.py` (novo), `petbits/states/pet_state.py`,
  `petbits/pages/inicio.py`, `petbits/petbits.py`; `tests/test_proximo.py`.
- Backend: nenhum; usa o `GET agendamentos` que já existe.
