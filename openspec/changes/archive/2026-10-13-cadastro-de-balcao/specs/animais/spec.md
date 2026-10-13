# Spec Delta

## MODIFIED Requirements

### Requirement: O dono do animal vem do servidor

**No caminho do tutor**, o dono de um animal SHALL ser determinado a partir
da credencial de quem faz a requisição, e qualquer identificador de tutor
presente no corpo ou na URL MUST ser ignorado, em todos os verbos.

**No caminho da equipe**, o dono SHALL vir da requisição — a clínica cadastra
o animal de outra pessoa —, e MUST ser conferido contra o banco antes de
qualquer gravação. Trocar "ignorar o que mandaram" por "conferir o que
mandaram" vale **apenas** para o caminho da equipe.

#### Scenario: Dono forjado na criação

- **WHEN** a requisição de criação **pelo caminho do tutor** inclui o
  identificador de outro tutor
- **THEN** o animal é criado para o tutor da credencial, não para o informado

#### Scenario: Tentativa de doar o animal na edição

- **WHEN** a requisição de edição inclui o identificador de outro tutor
- **THEN** o animal permanece com o tutor que já o possuía

#### Scenario: Conta sem ficha de tutor tenta cadastrar

- **WHEN** uma conta autenticada que não possui ficha de tutor tenta criar um
  animal **pelo caminho do tutor**
- **THEN** a operação é recusada com mensagem explícita sobre a própria conta
- **AND** nenhum animal é gravado

#### Scenario: A equipe informa de quem é o animal

- **WHEN** a equipe cadastra um animal informando um tutor existente
- **THEN** o animal é criado para o tutor informado

#### Scenario: A equipe informa um tutor que não existe

- **WHEN** a equipe cadastra um animal informando um identificador de tutor
  que não existe
- **THEN** a operação é recusada
- **AND** nenhum animal é gravado

#### Scenario: A equipe não informa tutor nenhum

- **WHEN** a equipe cadastra um animal sem informar o tutor
- **THEN** a operação é recusada
- **AND** nenhum animal órfão é criado

## ADDED Requirements

### Requirement: A equipe cadastra animal da clínica

A equipe SHALL criar um animal para um tutor existente, informando nome e
espécie; raça, nascimento, peso e observações são opcionais.

#### Scenario: Cadastro com os dados mínimos

- **WHEN** a equipe cadastra um animal com tutor, nome e espécie
- **THEN** ele passa a aparecer na lista de animais da clínica
- **AND** passa a aparecer também para o tutor dele

#### Scenario: Nome ou espécie ausentes

- **WHEN** o cadastro é enviado sem nome ou sem espécie
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Equipe comum também cadastra

- **WHEN** uma conta de equipe que não é da gerência cadastra um animal
- **THEN** a operação é aceita

#### Scenario: Tutor tenta o caminho da equipe

- **WHEN** uma conta de tutor tenta criar um animal pelo caminho da equipe
- **THEN** o backend recusa
- **AND** nada é gravado
