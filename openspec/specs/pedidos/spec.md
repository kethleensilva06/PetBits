# pedidos Specification

## Purpose

Define o Pedido — o que um cliente comprou da loja, e o que a clínica faz com
isso depois. Cobre as duas origens que levam ao mesmo registro: o pedido
feito pelo cliente no site e a **venda no balcão**, registrada pela equipe na
conta de quem está ali na frente.

O que esta capability governa é a **passagem de estado**: quais caminhos a
situação de um pedido pode seguir, quem pode movê-la, e o que cada passagem
faz com o estoque e com o pagamento. Cancelar devolve os itens; pagar é
registro da equipe, não do cliente.

## Requirements

### Requirement: A equipe vê os pedidos

A equipe SHALL ver todos os pedidos, do mais recente para o mais antigo,
podendo filtrar por situação, com cliente, telefone, itens, total, entrega,
endereço, forma de pagamento e situação. A lista MUST ser exclusiva da
equipe.

#### Scenario: Lista da equipe

- **WHEN** a equipe abre os pedidos
- **THEN** vê os pedidos de todos os clientes, com os itens de cada um

#### Scenario: Cliente pede a lista da clínica

- **WHEN** uma conta de cliente pede a lista de pedidos da clínica, fora da
  interface
- **THEN** o backend recusa

### Requirement: A situação só avança por caminhos válidos

A equipe SHALL mudar a situação de um pedido apenas pelos caminhos:
`pendente` para `pago`, `pronto_retirada`, `enviado` ou `cancelado`; `pago`
para `pronto_retirada`, `enviado` ou `cancelado`; `pronto_retirada` para
`entregue` ou `cancelado`; `enviado` para `entregue`. `pronto_retirada` MUST
valer só para retirada, e `enviado` só para entrega no endereço. `entregue` e
`cancelado` MUST NOT mudar mais.

#### Scenario: Pedido pronto para retirada

- **WHEN** a equipe marca como pronto um pedido pago de retirada
- **THEN** a situação passa a `pronto_retirada` e o cliente vê isso em "Meus
  pedidos"

#### Scenario: Caminho inválido

- **WHEN** a requisição tenta levar um pedido `entregue` para `pendente`, ou
  marcar como `enviado` um pedido de retirada, mesmo fora da interface
- **THEN** a operação é recusada e a situação não muda

### Requirement: Pagamento registrado pela equipe

Levar um pedido a `pago`, ou a `entregue` sem pagamento registrado, SHALL
gravar a data do pagamento. Um pedido já pago MUST manter a data original.

#### Scenario: Paga na retirada

- **WHEN** a equipe entrega um pedido `pronto_retirada` que tinha pagamento
  na loja e ainda não estava pago
- **THEN** a situação passa a `entregue` e a data do pagamento é registrada

### Requirement: Cancelar devolve o estoque

Cancelar um pedido SHALL devolver ao estoque a quantidade de cada item, numa
única transação: ou todo o estoque volta e o pedido fica cancelado, ou nada
muda.

#### Scenario: Cancelamento

- **WHEN** a equipe cancela um pedido com 2 unidades de um produto
- **THEN** o estoque desse produto aumenta em 2 e o pedido fica `cancelado`

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
