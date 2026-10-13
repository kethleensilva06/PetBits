## REMOVED Requirements

### Requirement: Entrada com e-mail e senha

**Reason**: As abas Cliente/Colaborador foram substituídas por duas páginas de
entrada separadas, a pedido da clínica. O comportamento que o requisito
garantia — verificação única, recusa idêntica, destino só depois da aceitação
e conta de tutor nunca levada à equipe — passa inteiro para os requisitos
"Entrada de clientes e entrada da equipe" e "Destino depois da entrada".

**Migration**: Quem usava a aba Cliente usa `/entrar`; quem usava a aba
Colaborador usa `/entrar/equipe`.

## ADDED Requirements

### Requirement: Página inicial pública

O sistema SHALL ter uma página inicial pública que apresenta o PetBits e leva
à entrada de clientes, à entrada da equipe e à criação de conta. Quem abre o
endereço principal do sistema sem sessão SHALL ser conduzido a ela.

#### Scenario: Visitante abre o sistema

- **WHEN** alguém sem sessão abre o endereço principal do sistema
- **THEN** vê a página inicial, com os caminhos para clientes, para a equipe
  e para criar conta
- **AND** nenhum dado de cliente ou da clínica é carregado

#### Scenario: Quem já entrou

- **WHEN** alguém com sessão abre a página inicial
- **THEN** é levado à sua área

### Requirement: Entrada de clientes e entrada da equipe

O sistema SHALL autenticar por e-mail e senha em duas páginas, a entrada de
clientes e a entrada da equipe, ambas com a mesma verificação de credencial.
Credenciais inválidas MUST produzir a mesma mensagem nas duas, exista o
e-mail ou não. A página usada MUST NOT ser enviada ao servidor. Só a entrada
de clientes oferece criar conta.

#### Scenario: Senha incorreta

- **WHEN** a pessoa informa um e-mail existente com a senha errada, em
  qualquer das entradas
- **THEN** a entrada é recusada com uma mensagem genérica de credenciais
  inválidas

#### Scenario: E-mail inexistente

- **WHEN** a pessoa informa um e-mail que não tem conta
- **THEN** a entrada é recusada com **a mesma** mensagem do cenário anterior
- **AND** a resposta não permite distinguir os dois casos

#### Scenario: A página escolhida não muda a verificação

- **WHEN** as mesmas credenciais são enviadas pelas duas entradas
- **THEN** o resultado da verificação é idêntico: mesma recusa ou mesma
  aceitação, mesma mensagem e mesmo tempo de resposta

### Requirement: Destino depois da entrada

Depois de a credencial ser confirmada, a entrada da equipe SHALL levar uma
conta de equipe à gerência e a entrada de clientes SHALL levar uma conta de
cliente à área de cliente. Quem usa a entrada que não é a sua, ou não tem
papel conhecido, MUST ser recusado sem guardar a sessão.

#### Scenario: Cliente entra

- **WHEN** uma conta de cliente informa e-mail e senha corretos na entrada de
  clientes
- **THEN** a sessão é iniciada e ela vai para a área de cliente

#### Scenario: Funcionário entra na gerência

- **WHEN** uma conta de equipe informa e-mail e senha corretos na entrada da
  equipe
- **THEN** a sessão é iniciada e ela vai para a gerência

#### Scenario: Funcionário pela entrada de clientes

- **WHEN** uma conta de equipe acerta a senha na entrada de clientes
- **THEN** a sessão não é iniciada e a mensagem orienta a usar a entrada da
  equipe

#### Scenario: Conta sem papel de equipe pela entrada da equipe

- **WHEN** uma conta de cliente acerta a senha na entrada da equipe
- **THEN** a sessão não é iniciada e a mensagem orienta a usar a entrada de
  clientes

#### Scenario: Conta sem papel definido

- **WHEN** uma conta sem papel conhecido acerta a senha em qualquer entrada
- **THEN** a sessão não é iniciada e a mensagem orienta a procurar a clínica

### Requirement: Funcionário não usa a área de cliente

Uma conta de equipe que abre um endereço da área de cliente SHALL ser levada
à gerência, sem que nenhum dado de cliente seja carregado.

#### Scenario: Funcionário abre a área de cliente pelo endereço

- **WHEN** uma conta de equipe com sessão abre `/` ou `/agenda`
- **THEN** ela é levada à gerência
- **AND** nenhuma requisição de dados de cliente é feita
