# Spec Delta

## ADDED Requirements

### Requirement: A equipe cadastra tutor de balcão

A equipe SHALL criar um tutor informando nome e documento; contato e endereço
são opcionais. O tutor criado assim MUST NOT receber conta de acesso.

A recusa por documento já cadastrado MAY ser explícita neste caminho, por ele
ser autenticado e restrito à equipe — ao contrário do cadastro público, onde
a recusa é genérica de propósito.

#### Scenario: Cadastro com os dados mínimos

- **WHEN** a equipe cadastra um tutor informando nome e documento
- **THEN** ele passa a aparecer na lista de tutores da clínica
- **AND** nenhuma conta de acesso é criada

#### Scenario: Documento ausente

- **WHEN** o cadastro é enviado sem documento
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Documento já pertence a outro tutor

- **WHEN** a equipe informa um documento que já está cadastrado
- **THEN** a operação é recusada antes de qualquer gravação
- **AND** a mensagem diz que o documento já está cadastrado

#### Scenario: Documento com pontuação

- **WHEN** a equipe informa o mesmo documento de outro tutor, escrito com
  pontuação diferente
- **THEN** a operação é recusada do mesmo jeito

#### Scenario: Tutor de balcão não alcança o aplicativo

- **WHEN** um tutor criado pela equipe existe na base
- **THEN** não há credencial associada a ele
- **AND** nenhuma sessão pode ser iniciada em nome dele

#### Scenario: Equipe comum também cadastra

- **WHEN** uma conta de equipe que não é da gerência cadastra um tutor
- **THEN** a operação é aceita

#### Scenario: Tutor tenta cadastrar tutor

- **WHEN** uma conta de tutor tenta criar um tutor, fora da interface
- **THEN** o backend recusa
- **AND** nada é gravado
