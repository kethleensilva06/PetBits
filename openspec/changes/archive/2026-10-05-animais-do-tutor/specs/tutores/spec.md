# Spec Delta

## MODIFIED Requirements

### Requirement: Documento de identificação único

O sistema SHALL recusar a criação de um tutor cujo documento de identificação
já pertença a outro tutor. Duas fichas para a mesma pessoa quebrariam o
histórico do animal. A recusa MUST NOT revelar qual dos dados já estava em
uso.

#### Scenario: Documento já cadastrado

- **WHEN** alguém tenta se cadastrar com um documento que já existe
- **THEN** a operação é recusada com uma mensagem genérica, que orienta a
  procurar a clínica
- **AND** a resposta não permite deduzir que foi o documento, e não o e-mail,
  que já estava cadastrado
- **AND** nenhum vínculo automático com a ficha existente é criado

#### Scenario: E-mail já cadastrado

- **WHEN** alguém tenta se cadastrar com um e-mail que já existe
- **THEN** recebe **a mesma** mensagem do cenário anterior
- **AND** a resposta não permite distinguir os dois casos

#### Scenario: A distinção fica no registro do servidor

- **WHEN** um cadastro é recusado por documento ou por e-mail duplicado
- **THEN** o motivo específico fica registrado no servidor, para diagnóstico
- **AND** não aparece na resposta enviada a quem pediu

#### Scenario: Recusa não deixa conta órfã

- **WHEN** o cadastro é recusado por documento duplicado
- **THEN** nenhuma conta de acesso permanece criada
- **AND** a pessoa pode tentar de novo com outro documento
