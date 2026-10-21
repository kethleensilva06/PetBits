## ADDED Requirements

### Requirement: Pedidos em andamento e finalizados

Meus pedidos SHALL separar os pedidos em andamento — aguardando pagamento,
pagos, prontos para retirada e enviados — dos finalizados — entregues e
cancelados —, estes fechados por padrão, com a quantidade à vista.

#### Scenario: Um pronto e um entregue

- **WHEN** a tutora tem um pedido pronto para retirada e outro entregue
- **THEN** o pronto aparece em Em andamento e o entregue em Finalizados, que começa fechado
