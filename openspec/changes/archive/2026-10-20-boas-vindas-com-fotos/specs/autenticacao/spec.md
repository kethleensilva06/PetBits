## MODIFIED Requirements

### Requirement: Página inicial pública

O sistema SHALL ter uma página inicial pública que apresenta o PetBits e leva
à entrada de clientes, à entrada da equipe e à criação de conta. Quem abre o
endereço principal do sistema sem sessão SHALL ser conduzido a ela. A página
SHALL apresentar a clínica com fotos reais: uma capa com os atalhos Entrar e
Criar conta, e os serviços — Clínica, Banho e tosa e Petshop —, cada um com
foto e texto curto. As fotos MUST ser as que acompanham o app, com crédito em
`assets/fotos/CREDITOS.md`, e a página MUST NOT fazer requisição ao Xano.

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
