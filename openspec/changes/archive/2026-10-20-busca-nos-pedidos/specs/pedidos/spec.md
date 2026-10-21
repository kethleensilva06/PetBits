## ADDED Requirements

### Requirement: A equipe procura pedidos

A tela de Pedidos da clínica SHALL ter um campo de busca que filtra a lista
já carregada pelo número do pedido, pelo nome ou telefone do cliente e pelos
produtos do pedido, junto com o filtro de situação e sem requisição ao
backend.

#### Scenario: Pelo número

- **WHEN** alguém da equipe digita "14" em Pedidos
- **THEN** aparece o pedido nº 14

#### Scenario: Pelo cliente e produto

- **WHEN** alguém da equipe digita "ana areia"
- **THEN** aparecem só os pedidos da Ana que têm areia
