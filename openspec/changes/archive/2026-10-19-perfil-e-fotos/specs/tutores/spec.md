## ADDED Requirements

### Requirement: O tutor altera os próprios dados

Um tutor autenticado SHALL alterar nome, telefone e endereço da própria
ficha. A ficha alterada MUST ser a do token, nunca uma indicada na
requisição. Nome MUST NOT ficar em branco. CPF e e-mail MUST NOT ser
alterados por este caminho.

#### Scenario: Troca de telefone

- **WHEN** a tutora muda o telefone no perfil e salva
- **THEN** a ficha dela passa a ter o novo telefone, e os outros dados ficam como estavam

#### Scenario: Nome em branco

- **WHEN** o tutor apaga o nome e salva
- **THEN** a alteração é recusada e o motivo é informado

#### Scenario: Tentativa de alterar o CPF

- **WHEN** uma requisição direta envia `documento` ou `email` junto com o telefone
- **THEN** documento e e-mail não mudam

#### Scenario: Conta sem ficha

- **WHEN** uma conta de equipe chama a alteração de perfil de tutor
- **THEN** é recusada, sem alterar ficha nenhuma

### Requirement: Foto de perfil do tutor

Um tutor autenticado SHALL enviar uma foto de perfil, que substitui a
anterior e aparece no avatar do cabeçalho. Só imagens JPG, PNG ou WebP de até
5 MB SHALL ser aceitas. Sem foto, o avatar mostra as iniciais do nome.

#### Scenario: Envio de foto

- **WHEN** o tutor envia uma foto JPG de 2 MB
- **THEN** a foto passa a aparecer no avatar do cabeçalho

#### Scenario: Arquivo que não é imagem

- **WHEN** o tutor envia um PDF ou uma imagem de 8 MB
- **THEN** o envio é recusado com o motivo, e a foto anterior continua
