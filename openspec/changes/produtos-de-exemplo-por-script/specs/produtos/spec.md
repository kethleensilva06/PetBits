## ADDED Requirements

### Requirement: Script cadastra produtos de exemplo

O projeto SHALL ter um script que entra com uma conta de equipe do arquivo
local de contas de teste e cadastra produtos de exemplo pelo mesmo cadastro
da tela da equipe. Produto cujo nome já exista no catálogo MUST ser pulado. A
senha da conta MUST NOT aparecer na saída.

#### Scenario: Catálogo vazio

- **WHEN** quem desenvolve roda o script com o catálogo vazio
- **THEN** 15 produtos ativos, com estoque, passam a aparecer na loja

#### Scenario: Rodar de novo

- **WHEN** o script roda com os produtos de exemplo já cadastrados
- **THEN** nenhum produto é duplicado

#### Scenario: Sem conta de equipe com senha

- **WHEN** o arquivo de contas de teste não tem conta de equipe com senha
- **THEN** o script para antes de qualquer requisição, explicando o que falta

#### Scenario: A conta não é de equipe

- **WHEN** a conta usada entra mas não tem papel de equipe
- **THEN** o script para sem cadastrar nada, explicando o motivo
