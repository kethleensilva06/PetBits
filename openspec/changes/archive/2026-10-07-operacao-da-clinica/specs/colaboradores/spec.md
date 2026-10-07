# Spec Delta

## Purpose

Define o Colaborador — quem trabalha na clínica — como registro do domínio:
seus dados, a função que exerce, e quem pode lê-los ou alterá-los. A função é
o que determina, mais adiante, quem pode executar cada tipo de serviço.

## ADDED Requirements

### Requirement: Registro de colaborador

O sistema SHALL manter, para cada colaborador, nome e função. Contato e data
de entrada na clínica são opcionais.

#### Scenario: Cadastro com os dados mínimos

- **WHEN** a equipe cadastra um colaborador informando nome e função
- **THEN** ele passa a aparecer na lista de colaboradores

#### Scenario: Nome ausente

- **WHEN** o cadastro é enviado sem nome
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Função ausente

- **WHEN** o cadastro é enviado sem função
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Campos opcionais em branco

- **WHEN** o cadastro é enviado sem contato e sem data de entrada
- **THEN** o colaborador é criado normalmente

### Requirement: A função vem de um conjunto fechado

A função de um colaborador SHALL ser uma entre **gerente**, veterinário,
tosador e atendente. Qualquer outro valor MUST ser recusado.

A função descreve **o que a pessoa faz na clínica**, e não o que ela alcança
no sistema. Gerente é um cargo, não um nível de permissão: quem administra o
sistema é definido pelo papel da **conta de acesso**, que é coisa separada e
continua sendo concedida fora da aplicação.

#### Scenario: Função reconhecida

- **WHEN** a equipe cadastra um colaborador com uma das funções previstas
- **THEN** o cadastro é aceito

#### Scenario: Função desconhecida

- **WHEN** a requisição informa uma função fora do conjunto previsto
- **THEN** a operação é recusada, mesmo feita fora da interface

### Requirement: Manter e consultar colaboradores

A equipe SHALL listar, consultar e alterar colaboradores.

#### Scenario: Lista de colaboradores

- **WHEN** a equipe pede a lista
- **THEN** recebe todos os colaboradores cadastrados

#### Scenario: Alteração de um colaborador

- **WHEN** a equipe altera os dados de um colaborador
- **THEN** os dados são atualizados
- **AND** os campos não mencionados permanecem com os valores que tinham

#### Scenario: Colaborador inexistente

- **WHEN** a equipe consulta ou altera um identificador que não existe
- **THEN** recebe a resposta de "não encontrado"

### Requirement: Colaborador é registro, não credencial

Um colaborador SHALL poder existir sem nenhuma conta de acesso associada, e
cadastrar um colaborador MUST NOT criar conta nem conceder acesso ao sistema.

#### Scenario: Colaborador sem conta

- **WHEN** a equipe cadastra um colaborador
- **THEN** nenhuma conta de acesso é criada
- **AND** nenhuma credencial é concedida

#### Scenario: Vários colaboradores sem conta coexistem

- **WHEN** vários colaboradores são cadastrados sem conta de acesso
- **THEN** todos permanecem válidos

### Requirement: Dados de colaborador não são informação de cliente

Os dados de contato e identificação de um colaborador SHALL ser acessíveis
apenas à equipe.

#### Scenario: Tutor tenta listar colaboradores

- **WHEN** uma conta de tutor pede a lista de colaboradores, fora da interface
- **THEN** o backend recusa
- **AND** nenhum nome, contato ou função é devolvido
