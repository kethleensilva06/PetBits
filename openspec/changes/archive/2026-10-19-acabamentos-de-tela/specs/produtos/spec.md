## ADDED Requirements

### Requirement: Busca e filtro na loja

A loja SHALL permitir buscar produto pelo nome, ignorando maiúsculas e
acentos, e filtrar por categoria. Buscar e filtrar SHALL NOT fazer requisição
ao backend. Quando nada casa, a loja SHALL dizer isso.

#### Scenario: Busca sem acento

- **WHEN** a tutora digita "racao" na busca
- **THEN** aparecem as rações, e só elas

#### Scenario: Filtro por categoria

- **WHEN** ela escolhe a categoria Brinquedo
- **THEN** aparecem só os brinquedos

#### Scenario: Nada encontrado

- **WHEN** a busca não casa com produto nenhum
- **THEN** a loja diz que nada foi encontrado

### Requirement: Quantidade no detalhe e carrinho no cabeçalho

O detalhe do produto SHALL permitir escolher a quantidade antes de adicionar,
limitada ao estoque disponível. O cabeçalho da área do cliente SHALL mostrar
um ícone de carrinho com o total de itens, que leva à loja.

#### Scenario: Levar três

- **WHEN** a tutora escolhe 3 no detalhe e adiciona
- **THEN** o carrinho passa a ter 3 daquele produto e o ícone do cabeçalho mostra 3

#### Scenario: Mais que o estoque

- **WHEN** ela tenta escolher mais do que o disponível
- **THEN** a quantidade para no estoque

### Requirement: CPF e telefone formatados

CPF e telefone SHALL ser formatados enquanto se digita, nos cadastros e nos
perfis: CPF como `000.000.000-00` e telefone como `(00) 0000-0000` ou
`(00) 00000-0000`. O que vai ao backend MUST continuar valendo para as regras
de lá (o CPF é normalizado no servidor).

#### Scenario: Digitar o CPF

- **WHEN** alguém digita `12345678909` no campo de CPF
- **THEN** o campo mostra `123.456.789-09`

#### Scenario: Digitar o celular

- **WHEN** alguém digita `11988887777` no telefone
- **THEN** o campo mostra `(11) 98888-7777`
