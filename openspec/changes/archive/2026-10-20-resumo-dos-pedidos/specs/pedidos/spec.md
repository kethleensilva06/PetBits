## ADDED Requirements

### Requirement: Resumo e exportação dos pedidos

A tela de Pedidos da clínica SHALL mostrar quantos pedidos estão na lista e o
total deles, respeitando o filtro e a busca, sem os cancelados no total, e
SHALL oferecer os mesmos pedidos num arquivo CSV para planilha. O arquivo MUST
NOT trazer telefone, documento nem endereço do cliente, e nada disso MUST
fazer requisição ao backend.

#### Scenario: Total dos pagos

- **WHEN** a gerência filtra "Pagos" com três pedidos de R$ 10, R$ 20 e R$ 30
- **THEN** o resumo mostra 3 pedidos e R$ 60,00

#### Scenario: Cancelado não soma

- **WHEN** a lista tem um pedido cancelado de R$ 50 e um entregue de R$ 20
- **THEN** o resumo mostra 2 pedidos e R$ 20,00, avisando que cancelados não entram no total

#### Scenario: Baixar CSV

- **WHEN** a gerência clica em Baixar CSV
- **THEN** recebe um arquivo com uma linha por pedido da tela, sem telefone do cliente
