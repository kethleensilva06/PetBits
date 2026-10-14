## MODIFIED Requirements

### Requirement: Página inicial pública

O sistema SHALL ter uma página inicial pública, no endereço principal do
sistema, que apresenta o PetBits e leva à entrada de clientes, à entrada da
equipe e à criação de conta.

#### Scenario: Visitante abre o sistema

- **WHEN** alguém sem sessão abre o endereço principal do sistema
- **THEN** vê a página inicial, com os caminhos para clientes, para a equipe
  e para criar conta
- **AND** nenhum dado de cliente ou da clínica é carregado

#### Scenario: Quem já entrou

- **WHEN** alguém com sessão abre a página inicial
- **THEN** é levado à sua área

### Requirement: Funcionário não usa a área de cliente

Uma conta de equipe que abre um endereço da área de cliente SHALL ser levada
à gerência, sem que nenhum dado de cliente seja carregado.

#### Scenario: Funcionário abre a área de cliente pelo endereço

- **WHEN** uma conta de equipe com sessão abre `/inicio` ou `/agenda`
- **THEN** ela é levada à gerência
- **AND** nenhuma requisição de dados de cliente é feita

## ADDED Requirements

### Requirement: Cada entrada tem endereço próprio

A entrada de clientes SHALL ficar em `/entrar/cliente` e a da equipe em
`/entrar/equipe`. A área do cliente logado SHALL ficar em `/inicio`. Os
endereços antigos `/entrar` e `/boas-vindas` MUST continuar levando às
páginas que os substituíram.

#### Scenario: Cliente abre a entrada de clientes

- **WHEN** alguém sem sessão abre `/entrar/cliente`
- **THEN** vê o formulário da entrada de clientes, com o caminho para criar
  conta

#### Scenario: Cliente entra e chega à sua área

- **WHEN** uma conta de cliente acerta a senha em `/entrar/cliente`
- **THEN** vai para `/inicio`

#### Scenario: Link antigo

- **WHEN** alguém abre `/entrar` ou `/boas-vindas`
- **THEN** é levado a `/entrar/cliente` ou a `/`, respectivamente
