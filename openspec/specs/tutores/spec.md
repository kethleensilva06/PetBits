# tutores

## Purpose

Define o Tutor como registro do domínio — a pessoa responsável por animais
atendidos pela clínica —, incluindo seus dados, a unicidade do documento de
identificação e o vínculo opcional com uma conta de acesso.

## Requirements

### Requirement: Registro de tutor

O sistema SHALL manter, para cada tutor, nome, documento de identificação e
formas de contato. Nome e documento MUST ser obrigatórios; telefone, e-mail e
endereço são opcionais.

#### Scenario: Ficha criada no cadastro

- **WHEN** uma pessoa conclui o cadastro informando nome, documento e contato
- **THEN** existe um tutor com exatamente esses dados

#### Scenario: Documento ausente

- **WHEN** o cadastro é enviado sem documento de identificação
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Contato opcional em branco

- **WHEN** o cadastro é enviado sem telefone e sem endereço
- **THEN** o tutor é criado normalmente

### Requirement: Documento de identificação único

O sistema SHALL recusar a criação de um tutor cujo documento de identificação
já pertença a outro tutor. Duas fichas para a mesma pessoa quebrariam o
histórico do animal.

#### Scenario: Documento já cadastrado

- **WHEN** alguém tenta se cadastrar com um documento que já existe
- **THEN** a operação é recusada
- **AND** a mensagem orienta a procurar a clínica, sem vincular
  automaticamente à ficha existente

#### Scenario: Recusa não deixa conta órfã

- **WHEN** o cadastro é recusado por documento duplicado
- **THEN** nenhuma conta de acesso permanece criada
- **AND** a pessoa pode tentar de novo com outro documento

### Requirement: Vínculo opcional com conta de acesso

Um tutor SHALL poder existir sem conta de acesso, para que a clínica possa
cadastrar quem é atendido no balcão e nunca usará o site. Quando existir, o
vínculo MUST apontar para no máximo uma conta.

#### Scenario: Tutor criado pelo cadastro público

- **WHEN** uma pessoa cria a própria conta pelo site
- **THEN** a conta de acesso e a ficha de tutor ficam vinculadas entre si

#### Scenario: Vários tutores sem conta coexistem

- **WHEN** dois ou mais tutores existem sem nenhuma conta de acesso associada
- **THEN** todos permanecem válidos
- **AND** a ausência de vínculo não impede a criação de novos tutores

#### Scenario: Uma conta não atende a dois tutores

- **WHEN** houver tentativa de vincular uma mesma conta de acesso a um
  segundo tutor
- **THEN** a operação é recusada

### Requirement: Acesso do tutor à própria ficha

Um usuário autenticado SHALL obter a ficha de tutor vinculada à própria
conta, e MUST NOT obter a de outro tutor.

#### Scenario: Tutor obtém a própria ficha

- **WHEN** um tutor autenticado solicita a sua ficha
- **THEN** recebe os dados do tutor vinculado à conta dele

#### Scenario: Tentativa de obter ficha alheia

- **WHEN** um tutor autenticado solicita a ficha de outro tutor
- **THEN** o backend recusa a requisição
- **AND** nenhum dado do outro tutor é devolvido

#### Scenario: Requisição sem sessão

- **WHEN** a ficha é solicitada sem credencial válida
- **THEN** o backend recusa a requisição

#### Scenario: Conta sem ficha vinculada

- **WHEN** um usuário autenticado que não possui ficha de tutor a solicita
- **THEN** o sistema responde que não há ficha, sem erro cru
- **AND** não devolve a ficha de outra pessoa
