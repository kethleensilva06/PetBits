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

Depois de a credencial ser aceita, a entrada de clientes SHALL levar à área de
cliente, e a entrada da equipe SHALL levar à gerência quando a conta for de
equipe e à área de cliente quando não for. Uma conta que não é de equipe MUST
NOT ser levada à gerência por nenhuma das entradas.

#### Scenario: Cliente entra

- **WHEN** uma pessoa informa e-mail e senha corretos na entrada de clientes
- **THEN** a sessão é iniciada e ela vai para a área de cliente

#### Scenario: Funcionário entra na gerência

- **WHEN** uma conta de equipe informa e-mail e senha corretos na entrada da
  equipe
- **THEN** a sessão é iniciada e ela vai para a gerência

#### Scenario: Funcionário pela entrada de clientes

- **WHEN** uma conta de equipe entra pela entrada de clientes
- **THEN** ela vai para a área de cliente

#### Scenario: Conta sem papel de equipe pela entrada da equipe

- **WHEN** uma conta que não é de equipe entra pela entrada da equipe
- **THEN** a sessão é iniciada normalmente
- **AND** ela vai para a área de cliente, sem aviso de que a conta não é da
  equipe
