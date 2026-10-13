# Spec Delta

## ADDED Requirements

### Requirement: Desligar e religar colaborador

A gerência SHALL marcar um colaborador como desligado, e voltar atrás. O
registro MUST permanecer na lista nos dois estados — a clínica precisa saber
quem já trabalhou nela, e esconder quem saiu esconderia o caminho de voltar.

Excluir um colaborador MUST NOT ser possível: quem saiu ainda é quem executou
os serviços já registrados.

#### Scenario: Desligar

- **WHEN** a gerência desliga um colaborador
- **THEN** ele passa a aparecer como desligado
- **AND** continua na lista

#### Scenario: Religar

- **WHEN** a gerência religa um colaborador desligado
- **THEN** ele volta a aparecer como ativo

#### Scenario: Desligar não apaga os outros dados

- **WHEN** um colaborador é desligado
- **THEN** nome, função e contato permanecem como estavam

#### Scenario: Equipe comum não desliga

- **WHEN** uma conta de equipe que não é da gerência tenta desligar um
  colaborador
- **THEN** a operação é recusada
- **AND** o estado dele permanece como estava

### Requirement: Dados opcionais podem ser esvaziados

A gerência SHALL poder apagar um dado opcional de um colaborador — contato,
e-mail ou data de entrada — e não apenas trocá-lo por outro valor.

#### Scenario: Apagar a data de entrada

- **WHEN** a gerência apaga a data de entrada de um colaborador e salva
- **THEN** o colaborador passa a não ter data de entrada

#### Scenario: Campo não mencionado continua intacto

- **WHEN** a alteração não menciona um campo
- **THEN** o valor dele permanece
