## ADDED Requirements

### Requirement: Cadastro de produto

A equipe SHALL cadastrar produtos com nome, categoria, preço, estoque e,
opcionalmente, marca, unidade de venda e descrição. O nome MUST NOT ficar em
branco, o preço MUST ser maior que zero e o estoque MUST ser maior ou igual a
zero. Todo produto nasce ativo.

#### Scenario: Produto cadastrado

- **WHEN** a equipe cadastra "Ração adulto 1 kg", categoria ração, R$ 49,90,
  estoque 20
- **THEN** o produto aparece no catálogo da equipe e, por estar ativo e com
  estoque, na loja do cliente

#### Scenario: Preço inválido

- **WHEN** o cadastro informa preço zero ou negativo, mesmo fora da interface
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Estoque negativo

- **WHEN** o cadastro ou a alteração informa estoque negativo
- **THEN** a operação é recusada

### Requirement: Alterar e desativar produto

A equipe SHALL alterar os dados de um produto, inclusive o estoque, e
ativá-lo ou desativá-lo. Os campos não mencionados MUST permanecer. Produto
desativado MUST NOT aparecer na loja nem ser comprado.

#### Scenario: Desativar

- **WHEN** a equipe desativa um produto
- **THEN** ele some da loja do cliente e uma compra que o inclua é recusada
- **AND** continua no catálogo da equipe, marcado como inativo

#### Scenario: Alteração parcial

- **WHEN** a equipe altera só o preço de um produto
- **THEN** os outros campos permanecem como estavam

### Requirement: O catálogo é da equipe

Criar e alterar produtos SHALL ser exclusivo da equipe.

#### Scenario: Cliente tenta alterar o catálogo

- **WHEN** uma conta de cliente tenta criar ou alterar um produto, fora da
  interface
- **THEN** o backend recusa e o catálogo permanece inalterado

### Requirement: A loja mostra o que pode ser comprado

O cliente SHALL ver, na loja, os produtos ativos com estoque maior que zero,
com nome, categoria, marca, unidade, preço, descrição e quantidade
disponível.

#### Scenario: Produto sem estoque

- **WHEN** o estoque de um produto chega a zero
- **THEN** ele deixa de aparecer na loja
