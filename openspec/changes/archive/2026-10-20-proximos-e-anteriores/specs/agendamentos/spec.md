## ADDED Requirements

### Requirement: Próximos e anteriores

Meus agendamentos SHALL separar os próximos — marcados ou em andamento que
ainda não terminaram, do mais perto para o mais longe — dos anteriores —
todos os outros, do mais recente para o mais antigo. Os anteriores SHALL ficar
fechados por padrão, com a quantidade à vista.

#### Scenario: Consulta amanhã e banho concluído

- **WHEN** a tutora tem uma consulta marcada amanhã e um banho concluído ontem
- **THEN** a consulta aparece em Próximos e o banho em Anteriores, que começa fechado

#### Scenario: Agendamento que já passou sem conclusão

- **WHEN** um agendamento marcado já terminou e ninguém o concluiu
- **THEN** ele aparece em Anteriores, e não em Próximos
