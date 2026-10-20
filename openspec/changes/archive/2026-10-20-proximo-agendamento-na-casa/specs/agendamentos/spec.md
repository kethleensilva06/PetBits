## ADDED Requirements

### Requirement: A casa mostra o próximo agendamento

A casa do cliente SHALL mostrar o próximo agendamento ainda não terminado
(marcado ou em andamento), com serviço, animal, dia, hora e profissional, e
quantos outros há depois dele. Sem agendamento futuro, SHALL oferecer
Agendar. Se a lista de agendamentos falhar, a casa MUST continuar mostrando
os animais, sem o cartão.

#### Scenario: Consulta amanhã

- **WHEN** a tutora tem uma consulta da Mel amanhã às 10h e um banho depois
- **THEN** a casa mostra "Consulta clínica · Mel", "Amanhã, 10:00", o profissional e "mais 1 agendamento"

#### Scenario: Nada marcado

- **WHEN** a tutora não tem agendamento futuro
- **THEN** a casa diz que não há nada marcado e oferece Agendar

#### Scenario: Cancelado não conta

- **WHEN** o único agendamento futuro foi cancelado
- **THEN** a casa diz que não há nada marcado
