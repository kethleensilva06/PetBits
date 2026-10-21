## ADDED Requirements

### Requirement: Agendar o retorno pelo histórico

Quando algum atendimento de um animal, sem contar os retificados, tem data de
retorno de hoje em diante, o histórico do tutor SHALL mostrar a mais próxima
e oferecer Agendar retorno, que abre a Agenda com o animal já escolhido e a
categoria Clínica. Retorno que já passou MUST NOT aparecer.

#### Scenario: Retorno daqui a uma semana

- **WHEN** a consulta da Mel tem retorno para daqui a 7 dias, e a vacina de depois não tem retorno
- **THEN** o histórico mostra a data e o botão, e o botão abre a Agenda com a Mel escolhida

#### Scenario: Retorno vencido

- **WHEN** todos os retornos já passaram
- **THEN** o histórico não sugere retorno
