## ADDED Requirements

### Requirement: O cliente cancela o próprio pedido

O cliente SHALL poder cancelar o próprio pedido enquanto ele está aguardando
pagamento e sem pagamento registrado. Cancelar SHALL devolver o estoque de
cada item na mesma transação. Pedido de outra pessoa MUST ser recusado como
inexistente, e pedido em qualquer outra situação MUST ser recusado sem
mudança.

#### Scenario: Cancelar antes de pagar

- **WHEN** a tutora cancela um pedido aguardando pagamento com 1 areia
- **THEN** o pedido fica cancelado e o estoque da areia aumenta em 1

#### Scenario: Pedido de outra pessoa

- **WHEN** um tutor tenta cancelar o pedido de outro, fora da interface
- **THEN** o backend responde que o pedido não foi encontrado, e nada muda

#### Scenario: Pedido já pago

- **WHEN** a tutora tenta cancelar um pedido pago
- **THEN** o backend recusa, e o pedido e o estoque não mudam
