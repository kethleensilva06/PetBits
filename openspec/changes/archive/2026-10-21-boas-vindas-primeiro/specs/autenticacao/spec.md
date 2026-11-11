## MODIFIED Requirements

### Requirement: Página inicial pública

O sistema SHALL ter uma página inicial pública que apresenta o PetBits e leva
à entrada de clientes, à entrada da equipe e à criação de conta, no endereço
principal do sistema (`/`). Quem abre o endereço principal sem sessão SHALL
ver essa página primeiro, antes de qualquer tela de cliente. A página SHALL
apresentar a clínica e seus serviços com as fotos que acompanham o app, e MUST
NOT fazer requisição ao Xano.

#### Scenario: Visitante abre o sistema

- **WHEN** alguém sem sessão abre o endereço principal do sistema
- **THEN** vê a página inicial, com os caminhos para clientes, para a equipe
  e para criar conta
- **AND** nenhum dado de cliente ou da clínica é carregado

#### Scenario: Quem já entrou

- **WHEN** alguém com sessão abre a página inicial
- **THEN** é levado à sua área

#### Scenario: Os serviços da clínica

- **WHEN** o visitante desce pela página inicial
- **THEN** vê Clínica, Banho e tosa e Petshop, cada um com uma foto e o que oferece

#### Scenario: Celular

- **WHEN** o visitante abre a página no celular
- **THEN** a foto da capa vem primeiro, e o título e os botões Entrar e Criar conta cabem na primeira tela

### Requirement: Funcionário não usa a área de cliente

Uma conta de equipe que abre um endereço da área de cliente SHALL ser levada
à gerência, sem que nenhum dado de cliente seja carregado.

#### Scenario: Funcionário abre a área de cliente pelo endereço

- **WHEN** uma conta de equipe com sessão abre `/animais` ou `/agenda`
- **THEN** ela é levada à gerência
- **AND** nenhuma requisição de dados de cliente é feita
