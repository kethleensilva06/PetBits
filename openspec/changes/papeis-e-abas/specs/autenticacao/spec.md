# Spec Delta

## MODIFIED Requirements

### Requirement: Entrada com e-mail e senha

O sistema SHALL autenticar a pessoa a partir de e-mail e senha. Credenciais
inválidas MUST produzir sempre a mesma mensagem, independentemente de o
e-mail existir ou não. A tela de entrada SHALL oferecer abas por público, e
todas MUST usar a mesma verificação de credencial.

A aba escolhida SHALL ser exigida, mas apenas **depois** de a credencial ter
sido confirmada. Antes disso, nada na resposta — status, corpo, tempo ou
número de requisições — MUST diferir entre as abas.

#### Scenario: Credenciais corretas

- **WHEN** a pessoa informa e-mail e senha corretos na aba do público dela
- **THEN** a sessão é iniciada
- **AND** a pessoa é levada à área correspondente ao papel da conta dela

#### Scenario: Senha incorreta

- **WHEN** a pessoa informa um e-mail existente com a senha errada
- **THEN** a entrada é recusada com uma mensagem genérica de credenciais
  inválidas

#### Scenario: E-mail inexistente

- **WHEN** a pessoa informa um e-mail que não tem conta
- **THEN** a entrada é recusada com **a mesma** mensagem do cenário anterior
- **AND** a resposta não permite distinguir os dois casos

#### Scenario: A aba escolhida não muda a verificação

- **WHEN** as mesmas credenciais **inválidas** são enviadas por abas
  diferentes da tela de entrada
- **THEN** o resultado é idêntico: mesma recusa, mesma mensagem, mesmo tempo
  de resposta e mesmo número de requisições
- **AND** não é possível deduzir o papel de uma conta pela aba em que ela
  falha

#### Scenario: Pessoa entra pela aba que não corresponde ao papel dela

- **WHEN** uma pessoa informa a senha **correta** numa aba que não é a do
  papel da conta dela
- **THEN** a entrada é recusada
- **AND** a pessoa é orientada a usar a outra aba
- **AND** nenhuma sessão permanece aberta

#### Scenario: Conta sem papel definido tenta entrar

- **WHEN** uma conta cujo papel está ausente ou fora dos valores previstos
  informa a senha correta
- **THEN** a entrada é recusada em qualquer das abas
- **AND** a mensagem orienta a procurar a clínica
- **AND** nenhuma sessão permanece aberta

## ADDED Requirements

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
