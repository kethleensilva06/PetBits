# colaboradores

## Purpose

Define o Colaborador — quem trabalha na clínica — como registro do domínio:
seus dados, a função que exerce, e quem pode lê-los ou alterá-los. A função é
o que determina, mais adiante, quem pode executar cada tipo de serviço.

## Requirements

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

A função de um colaborador SHALL ser uma entre gerente, veterinário, clínico
geral, tosador e atendente. Qualquer outro valor MUST ser recusado. A função
descreve o cargo, e MUST NOT determinar o que a conta alcança no sistema.

#### Scenario: Função reconhecida

- **WHEN** a equipe cadastra um colaborador com uma das funções previstas
- **THEN** o cadastro é aceito

#### Scenario: Função desconhecida

- **WHEN** a requisição informa uma função fora do conjunto previsto
- **THEN** a operação é recusada, mesmo feita fora da interface

#### Scenario: A função não concede acesso

- **WHEN** um colaborador é cadastrado com a função de gerente
- **THEN** nenhuma conta de acesso é criada nem alterada
- **AND** o que qualquer conta alcança continua vindo do papel dela

### Requirement: Manter e consultar colaboradores

Toda a equipe SHALL listar e consultar colaboradores. Apenas a **gerência**
SHALL criar e alterar.

#### Scenario: Lista de colaboradores

- **WHEN** qualquer conta de equipe pede a lista
- **THEN** recebe todos os colaboradores cadastrados

#### Scenario: Alteração de um colaborador

- **WHEN** uma conta de **gerência** altera os dados de um colaborador
- **THEN** os dados são atualizados
- **AND** os campos não mencionados permanecem com os valores que tinham

#### Scenario: Alteração por quem não é da gerência

- **WHEN** uma conta de equipe comum tenta criar ou alterar um colaborador
- **THEN** a operação é recusada
- **AND** os dados permanecem como estavam

#### Scenario: Colaborador inexistente

- **WHEN** a gerência consulta ou altera um identificador que não existe
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

### Requirement: Desligar e religar colaborador

A gerência SHALL marcar um colaborador como desligado, e voltar atrás. O
registro MUST permanecer na lista nos dois estados — a clínica precisa saber
quem já trabalhou nela, e esconder quem saiu esconderia o caminho de voltar.

Excluir um colaborador MUST NOT ser possível: quem saiu ainda é quem executou
os serviços já registrados.

#### Scenario: Desligar

- **WHEN** a gerência desliga um colaborador
- **THEN** ele passa a aparecer como desligado
- **AND** continua na lista

#### Scenario: Religar

- **WHEN** a gerência religa um colaborador desligado
- **THEN** ele volta a aparecer como ativo

#### Scenario: Desligar não apaga os outros dados

- **WHEN** um colaborador é desligado
- **THEN** nome, função e contato permanecem como estavam

#### Scenario: Equipe comum não desliga

- **WHEN** uma conta de equipe que não é da gerência tenta desligar um
  colaborador
- **THEN** a operação é recusada
- **AND** o estado dele permanece como estava

### Requirement: Dados opcionais podem ser esvaziados

A gerência SHALL poder apagar um dado opcional de um colaborador — contato,
e-mail ou data de entrada — e não apenas trocá-lo por outro valor.

#### Scenario: Apagar a data de entrada

- **WHEN** a gerência apaga a data de entrada de um colaborador e salva
- **THEN** o colaborador passa a não ter data de entrada

#### Scenario: Campo não mencionado continua intacto

- **WHEN** a alteração não menciona um campo
- **THEN** o valor dele permanece

### Requirement: O colaborador altera os próprios dados

Uma conta de equipe SHALL alterar o nome e o telefone da própria ficha de
colaborador. A ficha MUST ser a que tem o mesmo e-mail da conta do token,
nunca uma indicada na requisição. Nome MUST NOT ficar em branco. Função,
e-mail, data de entrada e ativo MUST NOT ser alterados por este caminho.
Alterar o nome SHALL alterar também o nome da conta de acesso.

#### Scenario: Troca de telefone

- **WHEN** a veterinária muda o telefone no perfil e salva
- **THEN** a ficha dela passa a ter o novo telefone, e a função continua a mesma

#### Scenario: Tentativa de mudar a própria função

- **WHEN** uma requisição direta envia `funcao` junto com o telefone
- **THEN** a função não muda

#### Scenario: Conta de equipe sem ficha

- **WHEN** uma conta de equipe cujo e-mail não está em ficha nenhuma abre o perfil
- **THEN** vê a troca de senha e o aviso para procurar a gerência, e a alteração de dados é recusada

#### Scenario: Conta de tutor

- **WHEN** uma conta de tutor chama o perfil de colaborador, fora da interface
- **THEN** o backend recusa, sem devolver dado de ficha nenhuma

#### Scenario: Nome novo depois de sair e entrar

- **WHEN** o colaborador muda o nome, sai e entra de novo
- **THEN** a saudação do topo usa o nome novo

### Requirement: Foto do colaborador

Uma conta de equipe com ficha SHALL enviar uma foto, que substitui a anterior
e aparece no avatar do topo da clínica. Só imagens JPG, PNG ou WebP de até
5 MB SHALL ser aceitas. Sem foto, o avatar mostra as iniciais.

#### Scenario: Envio de foto

- **WHEN** o colaborador envia uma foto WebP pelo perfil
- **THEN** a foto passa a aparecer no avatar do topo

#### Scenario: Arquivo que não é imagem

- **WHEN** ele envia um PDF
- **THEN** o envio é recusado com o motivo, e a foto anterior continua
