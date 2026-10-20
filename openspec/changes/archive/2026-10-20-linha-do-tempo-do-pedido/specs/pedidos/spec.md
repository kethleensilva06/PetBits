## MODIFIED Requirements

### Requirement: Meus pedidos

O cliente SHALL ver apenas os próprios pedidos, do mais recente para o mais
antigo, com itens, total, entrega, pagamento e situação. Cada pedido não
cancelado SHALL mostrar as etapas do seu caminho — Pedido recebido,
Pagamento, Pronto para retirada ou Enviado, Retirado ou Entregue —, com as
etapas feitas marcadas e a atual destacada. A etapa do pagamento SHALL ficar
feita só quando o pagamento foi registrado. O pedido cancelado SHALL dizer
que foi cancelado, sem as etapas.

#### Scenario: Dois clientes

- **WHEN** dois clientes têm pedidos
- **THEN** cada um vê só os seus, mesmo pedindo a lista fora da interface

#### Scenario: Pedido pago para entrega

- **WHEN** a cliente abre um pedido pago, com entrega no endereço
- **THEN** vê Pedido recebido e Pagamento feitos, Enviado como a etapa atual e Entregue por vir

#### Scenario: Pronto antes de pagar

- **WHEN** um pedido de retirada com pagamento na loja está pronto para retirada e ainda não foi pago
- **THEN** Pronto para retirada aparece feito, Retirado como a atual, e o pagamento como "Pagar na retirada", não feito

#### Scenario: Pedido cancelado

- **WHEN** o pedido foi cancelado
- **THEN** ele não mostra etapas, e diz que foi cancelado e que os itens voltaram ao estoque
