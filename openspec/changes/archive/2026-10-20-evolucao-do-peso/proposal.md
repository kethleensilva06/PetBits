## Why

Cada atendimento registra o peso do animal, mas o histórico só o mostra
solto em cada registro. Para saber se a Mel engordou ou emagreceu, é preciso
ler a linha do tempo inteira e fazer a conta.

## What Changes

- No alto do histórico (da equipe e do tutor), um quadro **Peso**: o último
  peso, com a data, e a diferença para a pesagem anterior ("+0,5 kg desde
  12/09/2026"), e barras com as últimas seis pesagens.
- Registro retificado não conta: vale a correção.
- Sem pesagem, o quadro não aparece. Calculado na tela, sem requisição.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `historico-clinico`: o histórico mostra a evolução do peso.

## Impact

- Código: `petbits/historico.py`, `petbits/states/historico_state.py`,
  `petbits/pages/historico.py`; `tests/test_historico.py`.
