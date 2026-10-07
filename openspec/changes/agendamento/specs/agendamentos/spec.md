## ADDED Requirements

### Requirement: Horários livres de um dia

O tutor SHALL poder consultar, para um serviço e um dia, os horários de início
em que existe pelo menos um profissional compatível livre durante toda a
duração do serviço. Os horários MUST ser múltiplos de 30 minutos, MUST estar
no futuro e o atendimento inteiro MUST caber no horário de funcionamento.

#### Scenario: Dia útil sem agendamentos

- **WHEN** o tutor consulta uma segunda-feira futura para um serviço de 30
  minutos, sem nenhum agendamento naquele dia
- **THEN** recebe os horários das 8h00 às 17h30, de 30 em 30 minutos

#### Scenario: O fim do atendimento precisa caber no expediente

- **WHEN** o tutor consulta um sábado para um serviço de 90 minutos
- **THEN** o último horário oferecido é 10h30, porque o sábado fecha às 12h

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

### Requirement: Marcar um agendamento

O tutor SHALL poder marcar um agendamento para um animal **dele**, informando
serviço, dia e hora de início e, opcionalmente, observações. O sistema MUST
atribuir um profissional ativo da função compatível com a categoria do serviço
— veterinário ou clínico geral para `clinica`, tosador para `banho_tosa` — que
esteja livre durante todo o intervalo. O agendamento nasce com a situação
**marcado**.

#### Scenario: Agendamento aceito

- **WHEN** o tutor marca um serviço de clínica para um animal dele num horário
  livre
- **THEN** o agendamento é criado como marcado, com um veterinário ou clínico
  geral atribuído
- **AND** passa a aparecer em "Meus agendamentos"

#### Scenario: Animal de outro tutor

- **WHEN** a requisição informa um animal que não é do tutor autenticado
- **THEN** a operação é recusada e nada é criado

#### Scenario: Horário fora do expediente

- **WHEN** a requisição informa um início fora do horário de funcionamento, ou
  cujo fim passe do fechamento, mesmo feita fora da interface
- **THEN** a operação é recusada

#### Scenario: Horário no passado ou fora da grade

- **WHEN** a requisição informa um início no passado, ou que não seja múltiplo
  de 30 minutos
- **THEN** a operação é recusada

#### Scenario: Serviço sem categoria

- **WHEN** a requisição informa um serviço sem categoria
- **THEN** a operação é recusada

### Requirement: Dois agendamentos não se sobrepõem no mesmo profissional

Um profissional MUST NOT ter dois agendamentos não cancelados cujos intervalos
se cruzem. O intervalo ocupado vai do início até o início mais a duração do
serviço, e dois intervalos se cruzam quando um começa antes de o outro
terminar.

#### Scenario: Todos os profissionais ocupados

- **WHEN** todos os profissionais compatíveis já têm agendamento que cruza o
  intervalo pedido
- **THEN** a operação é recusada com a mensagem de que o horário não está mais
  disponível

#### Scenario: Intervalos encostados

- **WHEN** um profissional tem um agendamento das 9h00 às 10h00 e é pedido um
  das 10h00 às 10h30
- **THEN** os dois podem ser do mesmo profissional

#### Scenario: Cancelado libera o intervalo

- **WHEN** um agendamento foi cancelado
- **THEN** o intervalo dele pode ser marcado de novo

### Requirement: Meus agendamentos

O tutor SHALL ver apenas os agendamentos dos animais dele, com animal,
serviço, nome e função do profissional, início, fim e situação. Dados de
contato do profissional MUST NOT ser devolvidos.

#### Scenario: Lista do tutor

- **WHEN** o tutor abre a agenda
- **THEN** vê os agendamentos dos animais dele, incluindo os cancelados

#### Scenario: Dois tutores

- **WHEN** dois tutores têm agendamentos
- **THEN** cada um vê só os seus, mesmo pedindo a lista fora da interface

### Requirement: Cancelar até 24 horas antes

O tutor SHALL poder cancelar um agendamento marcado de um animal dele até 24
horas antes do início. Cancelar MUST mudar a situação para cancelado e
registrar quando, sem apagar o agendamento.

#### Scenario: Cancelamento dentro do prazo

- **WHEN** o tutor cancela um agendamento que começa daqui a dois dias
- **THEN** a situação passa a cancelado e o horário volta a ficar livre

#### Scenario: Menos de 24 horas

- **WHEN** o tutor tenta cancelar um agendamento que começa daqui a 5 horas
- **THEN** a operação é recusada com a orientação de falar com a clínica

#### Scenario: Agendamento de outro tutor

- **WHEN** a requisição pede o cancelamento de um agendamento de outro tutor
- **THEN** a resposta é a mesma de um agendamento inexistente, e nada muda

#### Scenario: Já cancelado

- **WHEN** o tutor tenta cancelar um agendamento já cancelado
- **THEN** a operação é recusada e nada muda

### Requirement: Agenda do dia para a equipe

A equipe SHALL ver os agendamentos de um dia, de todos os profissionais, com
horário, animal, tutor, serviço, profissional e situação. A agenda MUST ser
exclusiva da equipe.

#### Scenario: Agenda de um dia

- **WHEN** a equipe abre a agenda de um dia
- **THEN** vê os agendamentos daquele dia em ordem de horário, inclusive os
  cancelados, identificados como tal

#### Scenario: Tutor pede a agenda da clínica

- **WHEN** uma conta de tutor pede a agenda da clínica, fora da interface
- **THEN** o backend recusa
