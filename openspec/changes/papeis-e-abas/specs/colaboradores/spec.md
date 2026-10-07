# Spec Delta

## MODIFIED Requirements

### Requirement: Manter e consultar colaboradores

Toda a equipe SHALL listar e consultar colaboradores. Apenas a **gerência**
SHALL criar e alterar.

#### Scenario: Lista de colaboradores

- **WHEN** qualquer conta de equipe pede a lista
- **THEN** recebe todos os colaboradores cadastrados

#### Scenario: Alteração de um colaborador

- **WHEN** uma conta de **gerência** altera os dados de um colaborador
- **THEN** os dados são atualizados
- **AND** os campos não mencionados permanecem com os valores que tinham

#### Scenario: Alteração por quem não é da gerência

- **WHEN** uma conta de equipe comum tenta criar ou alterar um colaborador
- **THEN** a operação é recusada
- **AND** os dados permanecem como estavam

#### Scenario: Colaborador inexistente

- **WHEN** a gerência consulta ou altera um identificador que não existe
- **THEN** recebe a resposta de "não encontrado"
