## ADDED Requirements

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
