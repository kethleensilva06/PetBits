# desempenho Specification

## Purpose
TBD - created by archiving change telas-guardadas. Update Purpose after archive.

## Requirements

### Requirement: Leituras guardadas por tempo

O sistema SHALL guardar, por um tempo limitado, as leituras que mudam pouco,
separadas pela credencial de quem pediu, e SHALL servir o guardado só a quem
apresentar a mesma credencial. Nada do que é guardado SHALL ser gravado no
navegador. Painel, agenda e pedidos da clínica, ocupação do dia, históricos e a
confirmação da sessão SHALL ser sempre buscados na hora.

#### Scenario: Voltar a uma tela

- **GIVEN** a pessoa abriu a lista de animais há menos de 10 minutos
- **WHEN** ela abre a Agenda, que também lista os animais
- **THEN** os animais vêm do guardado, sem nova requisição ao backend

#### Scenario: Outra pessoa no mesmo servidor

- **WHEN** duas pessoas, com credenciais diferentes, abrem a mesma tela
- **THEN** cada uma recebe só os próprios dados

#### Scenario: Tempo vencido

- **WHEN** a pessoa abre a tela depois do tempo do grupo
- **THEN** a leitura é feita de novo no backend

### Requirement: Gravar mostra a mudança na hora

Toda gravação feita pela pessoa SHALL apagar, para a credencial dela, o
guardado dos assuntos que a gravação afeta.

#### Scenario: Cadastrar um animal

- **WHEN** a pessoa cadastra um animal
- **THEN** a lista de animais seguinte é buscada no backend e já mostra o novo

### Requirement: Sair apaga o guardado

Encerrar a sessão, por Sair ou por vencimento, SHALL apagar tudo o que estava
guardado daquela credencial.

#### Scenario: Sair

- **WHEN** a pessoa sai
- **THEN** nada guardado com a credencial dela é servido de novo

### Requirement: Atualizar na hora

As áreas do cliente e da equipe SHALL ter um botão Atualizar que apaga o
guardado da credencial e recarrega a tela.

#### Scenario: Ver o que outra pessoa mudou

- **WHEN** a pessoa toca em Atualizar
- **THEN** a tela é recarregada com tudo buscado de novo no backend

### Requirement: Filtros do backend com índice

Todo campo usado como filtro numa consulta do backend SHALL ter índice, sozinho
ou como primeiro campo de um índice composto, salvo tabelas de configuração
com poucas linhas (colaborador, serviço, produto).

#### Scenario: Histórico de um profissional

- **WHEN** o backend procura os atendimentos de um profissional
- **THEN** a consulta usa o índice de `atendimento.id_colaborador`

#### Scenario: Pedidos por período

- **WHEN** a equipe abre os pedidos dos últimos 90 dias
- **THEN** a consulta usa o índice de `pedido.created_at`
