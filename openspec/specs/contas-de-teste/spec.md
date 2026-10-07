# contas-de-teste

## Purpose

Define o atalho de desenvolvimento que lista contas de teste na tela de
entrada e preenche o formulário com uma delas: de onde as contas vêm, o que
chega ao navegador, e a garantia de que nada disso existe em produção.

## Requirements

### Requirement: Atalho de contas de teste na tela de entrada

Em modo de desenvolvimento, a tela de entrada SHALL abrir uma lista das
contas de teste quando a pessoa pressionar `Alt+1`, e SHALL fechá-la com
`Alt+1` de novo ou com `Esc`. A lista MUST mostrar, para cada conta, apenas o
rótulo e o e-mail — nunca a senha.

#### Scenario: Abrir a lista

- **WHEN** a pessoa está na tela de entrada, em modo de desenvolvimento, e
  pressiona `Alt+1`
- **THEN** a lista de contas de teste aparece no canto inferior esquerdo
- **AND** cada item mostra o rótulo e o e-mail da conta, sem a senha

#### Scenario: Fechar a lista

- **WHEN** a lista está aberta e a pessoa pressiona `Esc` ou `Alt+1`
- **THEN** a lista fecha e o formulário fica como estava

#### Scenario: A lista não depende da aba

- **WHEN** a pessoa abre a lista com a aba Cliente e depois com a aba
  Colaborador
- **THEN** a lista é a mesma nas duas

### Requirement: Escolher uma conta preenche o formulário

Escolher uma conta da lista SHALL preencher o e-mail e a senha do formulário
de entrada com os dessa conta e fechar a lista. A escolha MUST NOT iniciar a
sessão nem fazer requisição ao Xano: a entrada só acontece quando a pessoa
envia o formulário, pela mesma verificação de sempre.

#### Scenario: Conta escolhida

- **WHEN** a pessoa clica numa conta da lista
- **THEN** os campos E-mail e Senha ficam preenchidos com os dela
- **AND** a lista fecha
- **AND** nenhuma requisição é feita ao Xano até a pessoa clicar em Entrar

#### Scenario: Conta com senha errada no arquivo

- **WHEN** a pessoa escolhe uma conta cuja senha no arquivo está desatualizada
  e envia o formulário
- **THEN** a recusa é a mesma de qualquer credencial inválida

### Requirement: As contas vêm de um arquivo local não versionado

As contas de teste SHALL ser lidas de `contas-de-teste.local.txt`, na raiz do
projeto, que MUST estar no `.gitignore`. Nenhuma credencial de teste MUST
aparecer no código, nos arquivos versionados ou no pacote enviado ao
navegador; a senha MUST sair do backend apenas no preenchimento da conta
escolhida.

#### Scenario: Arquivo ausente

- **WHEN** o arquivo não existe e a pessoa abre a lista
- **THEN** a lista mostra como criar o arquivo, em vez de contas
- **AND** a tela de entrada continua funcionando normalmente

#### Scenario: Senha fora do navegador até a escolha

- **WHEN** a lista está aberta e nenhuma conta foi escolhida
- **THEN** nenhuma senha do arquivo chegou ao navegador

#### Scenario: Arquivo fora do repositório

- **WHEN** o arquivo existe na raiz do projeto
- **THEN** o git o ignora e ele não aparece entre as alterações a versionar

### Requirement: O atalho não existe em produção

Em modo de produção, a lista de contas de teste MUST NOT ser montada na tela
de entrada, e o preenchimento por conta de teste MUST ser recusado pelo
backend, mesmo que o evento chegue por outro caminho.

#### Scenario: Alt+1 em produção

- **WHEN** a aplicação roda em modo de produção e a pessoa pressiona `Alt+1`
  na tela de entrada
- **THEN** nada aparece

#### Scenario: Evento forjado em produção

- **WHEN** em modo de produção chega ao backend um pedido de preenchimento por
  conta de teste
- **THEN** o pedido é ignorado e nenhum campo é preenchido
