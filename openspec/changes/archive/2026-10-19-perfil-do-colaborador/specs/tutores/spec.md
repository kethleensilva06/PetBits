## MODIFIED Requirements

### Requirement: O tutor altera os próprios dados

Um tutor autenticado SHALL alterar nome, telefone e endereço da própria
ficha. A ficha alterada MUST ser a do token, nunca uma indicada na
requisição. Nome MUST NOT ficar em branco. CPF e e-mail MUST NOT ser
alterados por este caminho. Alterar o nome SHALL alterar também o nome da
conta de acesso, de onde vem a saudação.

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

#### Scenario: Nome novo depois de sair e entrar

- **WHEN** a tutora muda o nome no perfil, sai e entra de novo
- **THEN** a saudação usa o nome novo
