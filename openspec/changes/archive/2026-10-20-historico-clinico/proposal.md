## Why

O PetBits existe para tirar o histórico do animal da ficha de papel — é o
objetivo nº 2 da visão do projeto — e ele ainda não existe. A clínica marca
e cancela consultas, mas o que aconteceu na consulta não fica em lugar
nenhum: quando o tutor troca de veterinário, o que foi feito antes depende de
alguém lembrar. E o tutor, para saber a última vacina, precisa ligar.

## What Changes

- **Atendimento** (o prontuário, no vocabulário da clínica), como o modelo de
  domínio descreve: animal, colaborador que atendeu, data, motivo,
  diagnóstico, tratamento realizado, peso no dia e data de retorno.
- **A equipe registra** o atendimento pela lista de animais da clínica (vale
  para emergência, sem agendamento) ou direto do agendamento, na agenda do
  dia; registrar a partir do agendamento o marca como **concluído**.
- **Nada se apaga nem se edita.** Corrigir é registrar uma **retificação**,
  que aponta para o atendimento corrigido; o original continua visível,
  marcado como retificado. Não há endpoint de alterar nem de remover.
- **O tutor lê** o histórico dos animais dele, numa linha do tempo, na casa.
  Vê o nome e a função de quem atendeu, nunca o contato.
- Quem atende tem de ser veterinário ou clínico geral, ativo.

## Capabilities

### New Capabilities

- `historico-clinico`: registrar, retificar e ler os atendimentos de um animal.

### Modified Capabilities

- `agendamentos`: o agendamento passa a ser concluído quando o atendimento é
  registrado a partir dele.

## Fora do escopo

- Anexos (exames, imagens) no atendimento — continuam fora do escopo do
  projeto.
- Receita impressa, carteira de vacinação em PDF, lembrete de retorno por
  e-mail.
- O tutor escrever no histórico.
- Situação "em andamento" no agendamento.

## Impact

- Xano: tabela nova `atendimento`; endpoints `POST equipe/atendimentos`,
  `GET equipe/animais/{pet_id}/historico`, `GET pet/{pet_id}/historico`;
  `equipe/agenda` passa a devolver `id_pet` e `id_colaborador`.
- Reflex: diálogo de histórico e de registro na área da clínica (animais e
  agenda); linha do tempo no cartão do animal da casa.
- Docs: `docs/project-overview.md` marca o histórico como entregue.
