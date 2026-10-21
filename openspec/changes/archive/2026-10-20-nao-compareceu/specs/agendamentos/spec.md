## ADDED Requirements

### Requirement: Não compareceu

A equipe SHALL poder registrar que o animal não compareceu a um agendamento
marcado cujo horário já começou. O agendamento SHALL passar à situação "Não
compareceu", visível para a equipe e para o tutor. Agendamento futuro,
cancelado, concluído ou já com falta MUST ser recusado sem mudança, e a
operação MUST ser exclusiva da equipe. Um agendamento com falta MUST NOT
virar atendimento.

#### Scenario: Animal não veio

- **WHEN** a consulta das 9h passou e a equipe marca Não compareceu
- **THEN** o agendamento aparece como "Não compareceu" na agenda da clínica e em Meus agendamentos

#### Scenario: Antes do horário

- **WHEN** a equipe tenta marcar falta num agendamento de amanhã, fora da interface
- **THEN** o backend recusa e nada muda

#### Scenario: Tutor tenta marcar falta

- **WHEN** uma conta de tutor chama a marcação de falta, fora da interface
- **THEN** o backend recusa

#### Scenario: Atendimento de agendamento com falta

- **WHEN** a equipe tenta registrar atendimento a partir de um agendamento com falta
- **THEN** o backend recusa
