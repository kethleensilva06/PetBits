## ADDED Requirements

### Requirement: Atendimento conclui o agendamento

Quando a equipe registra um atendimento a partir de um agendamento, o
agendamento SHALL passar a concluído. O agendamento MUST ser do mesmo animal
e MUST NOT estar cancelado nem já concluído; o profissional do agendamento
SHALL vir preenchido como quem atendeu.

#### Scenario: Concluir pela agenda

- **WHEN** a equipe registra o atendimento a partir do agendamento das 10h da Mel
- **THEN** o atendimento entra no histórico da Mel e o agendamento aparece como concluído na agenda

#### Scenario: Agendamento cancelado

- **WHEN** o agendamento indicado está cancelado
- **THEN** o registro é recusado e nada é gravado
