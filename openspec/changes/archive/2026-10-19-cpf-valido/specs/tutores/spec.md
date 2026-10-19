## ADDED Requirements

### Requirement: CPF válido pelos dígitos verificadores

O documento de identificação do tutor SHALL ser um CPF cujos dois dígitos
verificadores confiram pelo cálculo de módulo 11, e que não seja composto de
onze dígitos iguais. A conferência MUST acontecer no backend, antes de
qualquer gravação, tanto no cadastro público quanto no cadastro de balcão. A
pontuação (pontos, traço, espaço) SHALL ser ignorada.

#### Scenario: CPF com dígito verificador errado

- **WHEN** alguém se cadastra pelo site com o documento `123.456.789-00`
- **THEN** o cadastro é recusado com "CPF inválido. Confira os números."
- **AND** nenhuma conta de acesso nem ficha de tutor é criada

#### Scenario: Onze dígitos iguais

- **WHEN** o documento enviado é `111.111.111-11`
- **THEN** o cadastro é recusado da mesma forma, embora os dígitos verificadores confiram

#### Scenario: CPF válido com ou sem pontuação

- **WHEN** o documento enviado é um CPF válido, com pontuação ou só dígitos
- **THEN** o cadastro segue para as demais conferências (e-mail e documento já em uso)

#### Scenario: Balcão com CPF inválido

- **WHEN** a equipe cadastra um tutor no balcão com CPF inválido
- **THEN** a criação é recusada com a mesma mensagem e nenhuma ficha é gravada

#### Scenario: Chamada direta à API

- **WHEN** alguém envia CPF inválido direto ao `POST tutor/cadastro`, sem passar pela tela
- **THEN** a recusa é a mesma: a conferência da tela é só aviso, a regra é do backend
