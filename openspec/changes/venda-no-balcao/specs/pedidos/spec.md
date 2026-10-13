## ADDED Requirements

### Requirement: Venda no balcão

A equipe SHALL registrar uma venda presencial na conta de um cliente
cadastrado, com um ou mais itens. A venda MUST nascer entregue, com o
pagamento na loja registrado, origem `balcao`, e MUST baixar o estoque e
calcular preço e total pelas mesmas regras do pedido feito pelo site. A venda
no balcão MUST ser exclusiva da equipe.

#### Scenario: Venda registrada

- **WHEN** o atendente vende 1 unidade de um produto ao cliente Ana
- **THEN** o pedido nasce entregue, pago, com origem balcão
- **AND** aparece em "Meus pedidos" da Ana, e o estoque baixa em 1

#### Scenario: Estoque insuficiente no balcão

- **WHEN** o atendente tenta vender mais do que o estoque
- **THEN** a venda é recusada e nenhum estoque muda

#### Scenario: Cliente inexistente

- **WHEN** a requisição informa um cliente que não existe
- **THEN** a venda é recusada

#### Scenario: Cliente tenta registrar venda no balcão

- **WHEN** uma conta de cliente chama a venda no balcão, fora da interface
- **THEN** o backend recusa

### Requirement: Origem do pedido

Todo pedido SHALL ter origem `site` ou `balcao`. Pedidos feitos pela loja do
site MUST ter origem `site`.

#### Scenario: Pedido pelo site

- **WHEN** o cliente compra pela loja
- **THEN** o pedido tem origem `site`
