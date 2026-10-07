## ADDED Requirements

### Requirement: Conta sem ficha completa o próprio cadastro de cliente

Uma conta autenticada que não tem ficha de tutor SHALL poder criar a própria
ficha informando documento e, opcionalmente, telefone e endereço. A ficha
MUST ser vinculada à conta do token, com o nome e o e-mail da conta; nenhum
valor da requisição pode escolher a conta. O documento MUST ter 11 dígitos
depois de retirada a pontuação e MUST ser único. Uma conta MUST NOT ter mais
de uma ficha.

#### Scenario: Funcionário vira cliente

- **WHEN** uma conta de equipe sem ficha informa um CPF válido e ainda não
  usado
- **THEN** a ficha é criada vinculada à conta dela
- **AND** ela passa a poder cadastrar animais e marcar agendamentos

#### Scenario: Conta que já tem ficha

- **WHEN** uma conta que já tem ficha de tutor tenta criar outra, mesmo fora
  da interface
- **THEN** a operação é recusada e nenhuma ficha é criada

#### Scenario: CPF já cadastrado

- **WHEN** o CPF informado já pertence a outra ficha
- **THEN** a operação é recusada com a mesma mensagem genérica do cadastro
  público, que não confirma se o CPF é de um cliente

#### Scenario: CPF com pontuação

- **WHEN** o CPF é informado como `123.456.789-01`
- **THEN** ele é gravado como `12345678901`, e conta como o mesmo documento
  para a unicidade

#### Scenario: CPF incompleto

- **WHEN** o CPF informado não tem 11 dígitos
- **THEN** a operação é recusada e o motivo é informado
