## Why

O veterinário registra a data de retorno no atendimento, e o tutor a vê no
histórico do animal. Mas para marcar esse retorno ele fecha o histórico, vai
à Agenda e escolhe o animal e a categoria de novo.

## What Changes

- No histórico do tutor, quando algum atendimento (sem contar os retificados) tem
  retorno de hoje em diante, o mais próximo deles: "Retorno sugerido para
  dd/mm/aaaa" e o botão **Agendar retorno**.
- O botão fecha o histórico e abre a Agenda com o animal já escolhido e a
  categoria Clínica.
- Sem requisição a mais: a data vem do histórico que já foi carregado.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `historico-clinico`: o tutor agenda o retorno a partir do histórico.

## Impact

- Código: `petbits/historico.py`, `petbits/states/historico_state.py`,
  `petbits/pages/historico.py`; `tests/test_historico.py`.
