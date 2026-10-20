## MODIFIED Requirements

### Requirement: Horários livres de um dia

O tutor SHALL poder consultar, para um serviço e um dia, os horários de início
em que existe pelo menos um profissional compatível livre durante toda a
duração do serviço. Os horários MUST ser múltiplos de 30 minutos, MUST estar
no futuro e o atendimento inteiro MUST caber no horário de funcionamento:
segunda a sábado, das 8h às 18h.

#### Scenario: Dia útil sem agendamentos

- **WHEN** o tutor consulta uma segunda-feira futura para um serviço de 30
  minutos, sem nenhum agendamento naquele dia
- **THEN** recebe os horários das 8h00 às 17h30, de 30 em 30 minutos

#### Scenario: O fim do atendimento precisa caber no expediente

- **WHEN** o tutor consulta um sábado para um serviço de 90 minutos
- **THEN** o último horário oferecido é 16h30, porque o sábado fecha às 18h

#### Scenario: Domingo

- **WHEN** o tutor consulta um domingo
- **THEN** nenhum horário é oferecido

#### Scenario: Profissional ocupado em parte do intervalo

- **WHEN** o único tosador ativo está ocupado das 9h00 às 10h30 e o tutor
  consulta um serviço de banho e tosa de 60 minutos no mesmo dia
- **THEN** 8h30, 9h00, 9h30 e 10h00 não são oferecidos, porque cruzam o
  intervalo ocupado
- **AND** 8h00 (termina às 9h00) e 10h30 (começa no fim do ocupado) são
  oferecidos

#### Scenario: Nenhum profissional da função

- **WHEN** não há nenhum tosador ativo e o tutor consulta banho e tosa
- **THEN** nenhum horário é oferecido
