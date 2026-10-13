## ADDED Requirements

### Requirement: Saudação pelo nome

A interface SHALL cumprimentar a pessoa pelo primeiro nome, ignorando
títulos no começo do nome (Dr., Dra., Sr., Sra.).

#### Scenario: Nome com título

- **WHEN** a conta se chama "Dr. Otavio Lins"
- **THEN** a saudação é "Olá, Otavio!"

#### Scenario: Nome sem título

- **WHEN** a conta se chama "Ana Ribeiro"
- **THEN** a saudação é "Olá, Ana!"
