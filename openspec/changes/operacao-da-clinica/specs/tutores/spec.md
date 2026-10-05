# Spec Delta

## ADDED Requirements

### Requirement: A equipe enxerga os tutores da clínica

A equipe SHALL consultar todos os tutores cadastrados, inclusive os que não
possuem conta de acesso. Esse acesso MUST acontecer por um caminho próprio,
restrito à equipe.

#### Scenario: Equipe lista os tutores

- **WHEN** uma conta de equipe pede a lista de tutores
- **THEN** recebe todos os tutores cadastrados

#### Scenario: Tutor de balcão aparece

- **WHEN** existir um tutor sem conta de acesso
- **THEN** ele aparece na lista da equipe

#### Scenario: Tutor tenta listar os tutores

- **WHEN** uma conta de tutor pede a lista de tutores, fora da interface
- **THEN** o backend recusa
- **AND** nenhum dado de outro tutor é devolvido
