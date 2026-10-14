## ADDED Requirements

### Requirement: Categoria do serviço

O serviço SHALL poder ter uma categoria: `clinica` ou `banho_tosa`. A
categoria é opcional no cadastro e na alteração; qualquer outro valor MUST ser
recusado. Um serviço sem categoria MUST NOT ser oferecido ao tutor.

#### Scenario: Serviço com categoria

- **WHEN** a equipe cadastra um serviço com a categoria banho e tosa
- **THEN** o serviço é criado com essa categoria

#### Scenario: Categoria desconhecida

- **WHEN** a requisição informa a categoria "hospedagem"
- **THEN** a operação é recusada, mesmo feita fora da interface

#### Scenario: Serviço antigo sem categoria

- **WHEN** um serviço foi cadastrado antes de existir categoria
- **THEN** ele continua na lista da equipe
- **AND** não aparece para o tutor até a equipe definir a categoria

### Requirement: O tutor lê o catálogo

O tutor SHALL poder listar os serviços que têm categoria, com nome,
descrição, preço, duração e categoria.

#### Scenario: Catálogo para o tutor

- **WHEN** o tutor abre a agenda
- **THEN** vê os serviços com categoria, separados em clínica e banho e tosa
