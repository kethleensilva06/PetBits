## ADDED Requirements

### Requirement: O carrinho sobrevive a recarregar a página

O carrinho do cliente SHALL continuar com os mesmos produtos e quantidades
depois de recarregar a página, abrir outra aba ou o servidor reiniciar. Ao
abrir a loja, o carrinho SHALL ser conferido com o catálogo: produto fora da
loja sai, e quantidade acima do estoque é reduzida. Sair da conta MUST
esvaziar o carrinho.

#### Scenario: Recarregar a loja

- **WHEN** a tutora põe dois sachês no carrinho e aperta F5
- **THEN** o carrinho continua com os dois sachês

#### Scenario: Estoque menor

- **WHEN** o carrinho guardado tem 5 unidades e o estoque agora é 3
- **THEN** ao abrir a loja o carrinho fica com 3

#### Scenario: Outra pessoa no mesmo navegador

- **WHEN** a tutora sai da conta e outra pessoa entra no mesmo navegador
- **THEN** o carrinho da outra pessoa começa vazio
