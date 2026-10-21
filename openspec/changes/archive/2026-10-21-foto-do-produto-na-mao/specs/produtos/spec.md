## ADDED Requirements

### Requirement: Foto do produto ao cadastrar e removível

A equipe SHALL poder escolher a foto ao cadastrar um produto, e ela SHALL ser
gravada assim que o produto for salvo. A equipe SHALL poder remover a foto
enviada de um produto, que volta a usar a foto automática. Remover MUST ser
exclusivo da equipe.

#### Scenario: Cadastrar com foto

- **WHEN** a atendente cadastra um produto e escolhe uma foto antes de salvar
- **THEN** o produto aparece na loja com essa foto

#### Scenario: Remover a foto

- **WHEN** a equipe remove a foto enviada de um produto
- **THEN** a loja volta a mostrar a foto automática dele

#### Scenario: Tutor tenta remover

- **WHEN** uma conta de cliente chama a remoção, fora da interface
- **THEN** o backend recusa e a foto continua
