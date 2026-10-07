# servicos

## Purpose

Define o Serviço — o que a clínica oferece — com o preço e a **duração
estimada**. A duração é o que torna a agenda calculável: sem ela não há como
saber se dois atendimentos se sobrepõem.

## Requirements

### Requirement: Registro de serviço

O sistema SHALL manter, para cada serviço, nome, preço e duração estimada em
minutos. A descrição é opcional.

#### Scenario: Cadastro com os dados mínimos

- **WHEN** a equipe cadastra um serviço com nome, preço e duração
- **THEN** ele passa a aparecer na lista de serviços

#### Scenario: Nome ausente

- **WHEN** o cadastro é enviado sem nome
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Descrição em branco

- **WHEN** o cadastro é enviado sem descrição
- **THEN** o serviço é criado normalmente

### Requirement: Duração obrigatória e positiva

A duração estimada de um serviço SHALL ser obrigatória e maior que zero.

#### Scenario: Duração ausente

- **WHEN** o cadastro é enviado sem duração
- **THEN** a operação é recusada

#### Scenario: Duração zero ou negativa

- **WHEN** o cadastro informa duração zero ou negativa
- **THEN** a operação é recusada, mesmo feita fora da interface

#### Scenario: Duração não pode ser zerada na alteração

- **WHEN** a equipe altera um serviço informando duração zero
- **THEN** a operação é recusada
- **AND** a duração anterior permanece

### Requirement: Preço não pode ser negativo

O preço de um serviço SHALL ser maior ou igual a zero.

#### Scenario: Preço negativo

- **WHEN** o cadastro ou a alteração informa preço negativo
- **THEN** a operação é recusada

#### Scenario: Serviço gratuito

- **WHEN** o cadastro informa preço zero
- **THEN** o serviço é criado normalmente

### Requirement: Manter e consultar serviços

A equipe SHALL listar, consultar e alterar serviços.

#### Scenario: Lista de serviços

- **WHEN** a equipe pede a lista
- **THEN** recebe todos os serviços cadastrados

#### Scenario: Alteração de um serviço

- **WHEN** a equipe altera os dados de um serviço
- **THEN** os dados são atualizados
- **AND** os campos não mencionados permanecem com os valores que tinham

#### Scenario: Serviço inexistente

- **WHEN** a equipe consulta ou altera um identificador que não existe
- **THEN** recebe a resposta de "não encontrado"

### Requirement: O catálogo é da clínica

Manter o catálogo de serviços SHALL ser exclusivo da equipe.

#### Scenario: Tutor tenta alterar o catálogo

- **WHEN** uma conta de tutor tenta criar ou alterar um serviço, fora da
  interface
- **THEN** o backend recusa
- **AND** o catálogo permanece inalterado
