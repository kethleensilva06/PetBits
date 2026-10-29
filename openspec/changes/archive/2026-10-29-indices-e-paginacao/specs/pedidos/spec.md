## MODIFIED Requirements

### Requirement: A equipe vê os pedidos

A equipe SHALL ver os pedidos do período escolhido — últimos 90 dias (o
padrão), últimos 30 dias ou todo o período —, do mais recente para o mais
antigo, podendo filtrar por situação, com cliente, telefone, itens, total,
entrega, endereço, forma de pagamento e situação. A lista MUST ser exclusiva da
equipe.

#### Scenario: Lista da equipe

- **WHEN** a equipe abre os pedidos
- **THEN** vê os pedidos de todos os clientes dos últimos 90 dias, com os itens
  de cada um

#### Scenario: Todo o período

- **WHEN** a equipe escolhe "Todo o período"
- **THEN** vê os pedidos de toda a história da loja

#### Scenario: Vindo do painel

- **WHEN** a equipe abre os pedidos esperando a partir do painel
- **THEN** a lista mostra todo o período, e nenhum pedido contado no painel
  fica de fora

#### Scenario: Cliente pede a lista da clínica

- **WHEN** uma conta de cliente pede a lista de pedidos da clínica, fora da
  interface
- **THEN** o backend recusa
