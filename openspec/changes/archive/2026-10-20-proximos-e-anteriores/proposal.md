## Why

Em Meus agendamentos, o que vem pela frente e o que já passou ficam na mesma
lista, do mais novo para o mais velho: a consulta de amanhã aparece no meio de
banhos concluídos, cancelados e faltas, e o cliente lê as datas para achar o
que importa.

## What Changes

- Meus agendamentos em duas partes:
  - **Próximos**: marcados ou em andamento que ainda não terminaram, do mais
    perto para o mais longe.
  - **Anteriores**: concluídos, cancelados, faltas e os que já passaram, do
    mais recente para o mais antigo, fechados por padrão atrás de "Mostrar
    anteriores (N)".
- Sem próximos, a parte de cima diz que não há nada marcado e oferece marcar.
- A mesma regra de "ainda vem" do cartão da casa (`proximo-agendamento-na-casa`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `agendamentos`: Meus agendamentos separa próximos de anteriores.

## Impact

- Código: `petbits/proximo.py`, `petbits/states/agenda_state.py`,
  `petbits/pages/agenda.py`; `tests/test_proximo.py`.
