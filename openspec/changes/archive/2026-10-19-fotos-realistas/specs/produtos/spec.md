## ADDED Requirements

### Requirement: Detalhe do produto na loja

Na loja, clicar na foto ou no nome de um produto SHALL abrir o detalhe dele,
com a foto grande, categoria, marca, embalagem, descrição, preço,
disponibilidade, a quantidade já no carrinho e o botão de adicionar. Abrir o
detalhe SHALL NOT fazer requisição ao backend: os dados são os que a loja
já carregou.

#### Scenario: Abrir o detalhe

- **WHEN** a tutora clica na foto do "Arranhador de papelão"
- **THEN** abre o detalhe com a foto grande, a descrição "Com erva-de-gato inclusa." e o preço

#### Scenario: Adicionar pelo detalhe

- **WHEN** ela clica em "Adicionar ao carrinho" no detalhe
- **THEN** o produto entra no carrinho e o detalhe passa a mostrar "No carrinho: 1"

#### Scenario: Fechar

- **WHEN** ela aperta Esc ou o X
- **THEN** o detalhe fecha e a loja continua onde estava, com o carrinho intacto
