## ADDED Requirements

### Requirement: A ponta a ponta não deixa produto de teste à venda

O produto que a verificação de ponta a ponta cria SHALL ser desativado ao fim
da rodada em qualquer caso — passando, falhando ou interrompida por erro.

#### Scenario: Rodada que para no meio

- **WHEN** a verificação de ponta a ponta para por erro depois de criar o produto de verificação
- **THEN** o produto fica inativo, e a loja do cliente não o mostra
