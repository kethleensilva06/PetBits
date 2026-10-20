## ADDED Requirements

### Requirement: Desligar e religar serviço

A equipe SHALL desativar e reativar um serviço. Serviço inativo SHALL
continuar na lista da equipe, marcado como inativo, e MUST NOT ser oferecido
ao tutor nem aceito em agendamento novo. Serviço novo SHALL nascer ativo.
Agendamentos já marcados MUST NOT mudar.

#### Scenario: Desativar

- **WHEN** a equipe desativa o serviço "Sonda"
- **THEN** ele aparece na lista da equipe com o selo Inativo e o botão Ativar

#### Scenario: Tutor não vê serviço inativo

- **WHEN** um serviço com categoria é desativado
- **THEN** ele some da lista de serviços agendáveis do tutor

#### Scenario: Agendar serviço inativo

- **WHEN** uma requisição direta tenta agendar um serviço inativo
- **THEN** é recusada com "Este serviço não está disponível para agendamento." e nada é gravado

#### Scenario: Reativar

- **WHEN** a equipe reativa o serviço
- **THEN** ele volta a ser oferecido, se tiver categoria
