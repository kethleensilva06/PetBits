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

### Requirement: Entrada com e-mail e senha

O sistema SHALL autenticar a pessoa a partir de e-mail e senha. Credenciais
inválidas MUST produzir sempre a mesma mensagem, independentemente de o
e-mail existir ou não. A tela de entrada MAY oferecer abas por público, mas
todas MUST usar a mesma verificação de credencial. Depois de a credencial ser
aceita, a aba Cliente SHALL levar à área de cliente; a aba Colaborador SHALL
levar à área da equipe quando a conta for de equipe, e à área de cliente
quando não for. Uma conta que não é de equipe MUST NOT ser levada à área da
equipe por nenhuma aba.

#### Scenario: Credenciais corretas

- **WHEN** a pessoa informa e-mail e senha corretos
- **THEN** a sessão é iniciada
- **AND** a pessoa é levada à área definida pela aba e pelo papel da conta

#### Scenario: Senha incorreta

- **WHEN** a pessoa informa um e-mail existente com a senha errada
- **THEN** a entrada é recusada com uma mensagem genérica de credenciais
  inválidas

#### Scenario: E-mail inexistente

- **WHEN** a pessoa informa um e-mail que não tem conta
- **THEN** a entrada é recusada com **a mesma** mensagem do cenário anterior
- **AND** a resposta não permite distinguir os dois casos, para não revelar
  quem possui conta

#### Scenario: A aba escolhida não muda a verificação

- **WHEN** as mesmas credenciais são enviadas por abas diferentes da tela de
  entrada
- **THEN** o resultado é idêntico: mesma recusa ou mesma aceitação, mesma
  mensagem e mesmo tempo de resposta
- **AND** não é possível deduzir o papel de uma conta pela aba em que ela
  funciona

#### Scenario: Equipe entra pela aba Cliente

- **WHEN** uma conta de equipe autentica com sucesso pela aba Cliente
- **THEN** a sessão é iniciada
- **AND** ela é levada à área de cliente

#### Scenario: Equipe entra pela aba Colaborador

- **WHEN** uma conta de equipe autentica com sucesso pela aba Colaborador
- **THEN** ela é levada à área da equipe

#### Scenario: Pessoa entra pela aba que não corresponde ao papel dela

- **WHEN** uma conta de tutor autentica com sucesso pela aba Colaborador
- **THEN** a sessão é iniciada normalmente
- **AND** ela é levada à área de cliente, sem aviso — um aviso de "esta conta
  não é da equipe" seria uma diferença observável entre as abas

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
