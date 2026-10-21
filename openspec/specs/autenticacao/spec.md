# autenticacao

## Purpose

Define quem entra no sistema e como a sessão se comporta: criação de conta,
entrada, saída, persistência, expiração e a origem do papel do usuário. Não
define o que cada papel pode fazer em cada tela — apenas quem a pessoa é.

## Requirements

### Requirement: Criação pública de conta

O sistema SHALL permitir que qualquer visitante crie uma conta informando
nome, e-mail e senha. A conta criada por esse caminho MUST receber sempre o
papel de tutor, atribuído pelo servidor.

#### Scenario: Cadastro bem-sucedido

- **WHEN** um visitante envia nome, e-mail inédito e senha válida
- **THEN** a conta é criada com o papel de tutor
- **AND** a pessoa passa a estar autenticada, sem precisar entrar de novo

#### Scenario: E-mail já cadastrado

- **WHEN** um visitante tenta se cadastrar com um e-mail que já existe
- **THEN** o sistema recusa a operação e informa o motivo
- **AND** nenhum registro novo é criado

#### Scenario: Tentativa de escolher o próprio papel

- **WHEN** a requisição de cadastro inclui um papel diferente de tutor
- **THEN** o valor enviado é ignorado
- **AND** a conta é criada com o papel de tutor

### Requirement: Força mínima da senha

O sistema SHALL recusar senhas com menos de 8 caracteres, sem ao menos uma
letra ou sem ao menos um dígito, informando o motivo da recusa em português.

#### Scenario: Senha curta demais

- **WHEN** a senha informada tem menos de 8 caracteres
- **THEN** o cadastro é recusado
- **AND** a mensagem indica o tamanho mínimo exigido

#### Scenario: Senha sem dígito

- **WHEN** a senha informada não contém nenhum dígito
- **THEN** o cadastro é recusado
- **AND** a mensagem indica que falta um número

### Requirement: Persistência da sessão

Uma sessão iniciada SHALL permanecer válida enquanto a pessoa não sair e a
credencial não expirar, sobrevivendo a recarregamentos da página, a abas
novas e a reinícios do servidor de aplicação.

#### Scenario: Recarregar a página

- **WHEN** a pessoa autenticada recarrega a página
- **THEN** ela continua autenticada, sem informar as credenciais de novo

#### Scenario: Reiniciar o servidor de aplicação

- **WHEN** o servidor de aplicação é reiniciado e a pessoa recarrega a página
- **THEN** ela continua autenticada

#### Scenario: Abrir em outra aba

- **WHEN** a pessoa abre o sistema numa aba nova do mesmo navegador
- **THEN** ela continua autenticada

### Requirement: Encerramento da sessão

O sistema SHALL permitir encerrar a sessão a qualquer momento, descartando os
dados de sessão guardados no navegador.

#### Scenario: Sair do sistema

- **WHEN** a pessoa autenticada escolhe sair
- **THEN** a sessão é encerrada e ela vai para a tela de entrada
- **AND** os dados de sessão guardados no navegador ficam vazios

#### Scenario: Formulário limpo após sair

- **WHEN** a pessoa sai e a tela de entrada é exibida
- **THEN** os campos de e-mail e senha estão vazios, sem revelar quem usou o
  sistema antes

### Requirement: Credencial expirada

Quando a credencial deixar de valer, o sistema SHALL encerrar a sessão e
conduzir a pessoa à entrada com um aviso compreensível, nunca exibindo o erro
cru do backend.

#### Scenario: Credencial inválida ou vencida

- **WHEN** uma operação é recusada pelo backend por falta de autenticação
- **THEN** a sessão é encerrada
- **AND** a tela de entrada informa que a sessão expirou

#### Scenario: Falha de rede não encerra a sessão

- **WHEN** uma operação falha por indisponibilidade de rede ou do backend
- **THEN** a sessão **permanece** ativa
- **AND** a pessoa vê uma mensagem de falha de comunicação, não de sessão
  expirada

### Requirement: Proteção das rotas privadas

Rotas que exigem autenticação SHALL ser inacessíveis sem sessão válida, e a
recusa MUST ser garantida pelo backend, não apenas pela interface.

#### Scenario: Visitante abre rota privada

- **WHEN** alguém sem sessão acessa diretamente o endereço de uma rota
  privada
- **THEN** é conduzido à tela de entrada
- **AND** nenhum dado da rota é exibido nem carregado

#### Scenario: Requisição direta à API sem credencial

- **WHEN** uma requisição sem credencial é feita diretamente a um endpoint
  privado, fora da interface
- **THEN** o backend recusa a requisição
- **AND** nenhum dado é devolvido

### Requirement: Papel obtido do servidor

O papel do usuário SHALL ser determinado pelo registro no servidor a cada
verificação. Valores de papel guardados no navegador servem apenas para
adaptar a interface e MUST NOT conceder acesso.

#### Scenario: Papel alterado no servidor

- **WHEN** o papel de um usuário é alterado no banco e ele recarrega a página
- **THEN** o sistema passa a tratá-lo pelo papel novo

#### Scenario: Papel adulterado no navegador

- **WHEN** alguém altera o papel guardado no armazenamento local do navegador
- **THEN** nenhum acesso adicional é concedido
- **AND** o backend continua recusando o que aquele usuário não pode fazer

### Requirement: As telas de entrada e de cadastro nunca ficam travadas

Uma tentativa de entrar ou de criar conta que termine de qualquer forma —
aceita, recusada, com erro inesperado ou interrompida — MUST NOT deixar o
botão de envio desabilitado. Ao abrir a tela de entrada ou de cadastro, o
botão de envio SHALL estar disponível.

#### Scenario: Recusa libera o botão

- **WHEN** a pessoa envia credenciais inválidas
- **THEN** a recusa aparece e o botão Entrar volta a ficar disponível

#### Scenario: Erro inesperado libera o botão

- **WHEN** a tentativa de entrar termina com um erro que não é uma recusa do
  Xano
- **THEN** o botão Entrar volta a ficar disponível

#### Scenario: Tentativa interrompida não trava a próxima visita

- **WHEN** uma tentativa foi interrompida no meio, sem resposta, e a pessoa
  abre ou recarrega a tela de entrada
- **THEN** o botão Entrar está disponível

### Requirement: A senha digitada pode ser conferida

Todo campo de senha SHALL permitir ver o que foi digitado, e MUST começar
oculto.

#### Scenario: Revelar e ocultar

- **WHEN** a pessoa aciona o controle de visibilidade de um campo de senha
- **THEN** o que foi digitado fica legível
- **AND** acionar de novo volta a ocultar

#### Scenario: Começa oculto

- **WHEN** a tela de entrada ou a de cadastro é aberta
- **THEN** os campos de senha estão ocultos

### Requirement: Saudação pelo nome

A interface SHALL cumprimentar a pessoa pelo primeiro nome, ignorando
títulos no começo do nome (Dr., Dra., Sr., Sra.).

#### Scenario: Nome com título

- **WHEN** a conta se chama "Dr. Otavio Lins"
- **THEN** a saudação é "Olá, Otavio!"

#### Scenario: Nome sem título

- **WHEN** a conta se chama "Ana Ribeiro"
- **THEN** a saudação é "Olá, Ana!"

### Requirement: Página inicial pública

O sistema SHALL ter uma página inicial pública, no endereço principal do
sistema, que apresenta o PetBits e leva à entrada de clientes, à entrada da
equipe e à criação de conta. A página SHALL apresentar a clínica e seus
serviços com as fotos que acompanham o app, e MUST NOT fazer requisição ao
Xano.

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

- **WHEN** uma conta de equipe com sessão abre `/inicio` ou `/agenda`
- **THEN** ela é levada à gerência
- **AND** nenhuma requisição de dados de cliente é feita

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

### Requirement: Troca de senha pelo tutor

Um tutor autenticado SHALL trocar a própria senha informando a senha atual e
a nova duas vezes. A senha atual MUST ser conferida no servidor; a nova MUST
seguir a força mínima do cadastro.

#### Scenario: Troca correta

- **WHEN** o tutor informa a senha atual certa e uma nova válida, repetida igual
- **THEN** a senha muda, e a próxima entrada só funciona com a nova

#### Scenario: Senha atual errada

- **WHEN** a senha atual informada não confere
- **THEN** a troca é recusada e a senha continua a mesma

#### Scenario: Nova senha fraca

- **WHEN** a nova senha tem menos de 8 caracteres ou não tem letra e número
- **THEN** a troca é recusada com a regra da senha
