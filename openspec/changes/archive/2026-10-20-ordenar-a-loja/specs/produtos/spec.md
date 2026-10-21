## ADDED Requirements

### Requirement: Ordenar a loja

A loja do cliente SHALL poder ser ordenada por Em destaque (a ordem do
catálogo), Menor preço, Maior preço e Nome (A–Z), junto com a busca e o
filtro de categoria, sem requisição ao backend. A ordem por nome MUST ignorar
acentos e maiúsculas.

#### Scenario: Menor preço

- **WHEN** a tutora escolhe Menor preço
- **THEN** o produto mais barato aparece primeiro

#### Scenario: Com categoria

- **WHEN** a tutora filtra Higiene e escolhe Maior preço
- **THEN** vê só os produtos de higiene, do mais caro para o mais barato
