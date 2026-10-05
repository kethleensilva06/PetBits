# Spec Delta

## ADDED Requirements

### Requirement: A equipe enxerga os animais da clínica

A equipe SHALL consultar todos os animais atendidos pela clínica, com o tutor
responsável por cada um. Esse acesso MUST acontecer por um caminho próprio,
separado do caminho do tutor — que permanece restrito ao dono.

#### Scenario: Equipe lista os animais

- **WHEN** uma conta de equipe pede a lista de animais da clínica
- **THEN** recebe os animais de todos os tutores
- **AND** cada animal vem acompanhado do nome do tutor responsável

#### Scenario: Animal sem tutor válido aparece para a equipe

- **WHEN** existir um animal sem tutor válido na base
- **THEN** ele aparece para a equipe
- **AND** continua não aparecendo para nenhum tutor

#### Scenario: Tutor continua restrito aos seus

- **WHEN** uma conta de tutor pede a lista de animais pelo caminho do tutor
- **THEN** continua recebendo apenas os dele

#### Scenario: Tutor tenta o caminho da equipe

- **WHEN** uma conta de tutor usa o caminho da equipe, fora da interface
- **THEN** o backend recusa
- **AND** nenhum animal de outro tutor é devolvido
