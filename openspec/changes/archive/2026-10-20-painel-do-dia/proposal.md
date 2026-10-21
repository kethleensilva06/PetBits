## Why

O painel da clínica mostra só quatro contadores (colaboradores, serviços,
tutores e animais). Quem abre o sistema de manhã quer saber outra coisa: quem
vem hoje e quais pedidos esperam a equipe. Para isso, hoje é preciso abrir a
Agenda e os Pedidos, uma requisição e um clique cada.

## What Changes

- O painel abre com **Hoje**: os agendamentos do dia, em ordem de horário,
  com horário, animal, tutor, serviço, profissional e situação, e o atalho
  para a Agenda. Os cancelados não entram.
- O painel mostra **Pedidos esperando a equipe**: quantos estão aguardando
  pagamento, pagos (a separar) e prontos para retirada. Cada número abre a
  tela de Pedidos já filtrada.
- Os quatro contadores continuam, abaixo.
- Tudo continua numa requisição só: o `GET equipe/painel` passa a receber o
  dia e a devolver também a agenda do dia e as três contagens de pedidos.
  Sem telefone, documento nem endereço de tutor.

## Capabilities

### New Capabilities

- `painel-da-clinica`: o que o painel da clínica mostra e quanto ele custa.

### Modified Capabilities

Nenhuma.

## Fora do escopo

- Atualizar o painel sozinho de tempos em tempos (custaria requisições do
  orçamento da instância o dia todo).
- Agir sobre o agendamento ou o pedido pelo painel: as ações continuam na
  Agenda e nos Pedidos.

## Impact

- Backend: `apis/pet_bits/equipe_painel.xs` (entrada `dia`, agenda do dia e
  contagens de pedidos).
- Código: `petbits/xano.py`, `petbits/painel.py` (novo),
  `petbits/states/equipe_state.py`, `petbits/pages/equipe.py`;
  `tests/test_painel.py`.
- Documentação: `docs/project-overview.md` (roteiro).
