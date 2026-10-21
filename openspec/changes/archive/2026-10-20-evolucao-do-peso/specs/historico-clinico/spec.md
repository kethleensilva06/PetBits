## ADDED Requirements

### Requirement: Evolução do peso

O histórico de um animal SHALL mostrar o último peso registrado, com a data,
a diferença para a pesagem anterior e as últimas seis pesagens, para a equipe
e para o tutor. Atendimento retificado MUST NOT entrar na conta. Sem nenhuma
pesagem, o quadro SHALL NOT aparecer.

#### Scenario: Engordou

- **WHEN** a Mel pesou 28 kg em setembro e 28,5 kg em outubro
- **THEN** o histórico mostra "28,5 kg" e "+0,5 kg desde" a data de setembro

#### Scenario: Peso corrigido

- **WHEN** o atendimento de outubro foi retificado com 28,2 kg
- **THEN** o histórico usa 28,2 kg, e não o peso do registro retificado
