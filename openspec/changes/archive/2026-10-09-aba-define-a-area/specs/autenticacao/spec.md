## MODIFIED Requirements

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
