## ADDED Requirements

### Requirement: Filtros do backend com índice

Todo campo usado como filtro numa consulta do backend SHALL ter índice, sozinho
ou como primeiro campo de um índice composto, salvo tabelas de configuração
com poucas linhas (colaborador, serviço, produto).

#### Scenario: Histórico de um profissional

- **WHEN** o backend procura os atendimentos de um profissional
- **THEN** a consulta usa o índice de `atendimento.id_colaborador`

#### Scenario: Pedidos por período

- **WHEN** a equipe abre os pedidos dos últimos 90 dias
- **THEN** a consulta usa o índice de `pedido.created_at`
