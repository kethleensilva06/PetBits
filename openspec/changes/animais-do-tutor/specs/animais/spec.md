# Spec Delta

## Purpose

Define o Animal como registro do domínio — o bicho sob cuidado da clínica —,
seus dados, o vínculo obrigatório com um tutor, e quem pode lê-lo ou alterá-lo.
É aqui que o sistema declara, pela primeira vez, o que significa um dado ser
"de alguém".

## ADDED Requirements

### Requirement: Cadastro de animal

Um tutor autenticado SHALL cadastrar um animal informando nome e espécie.
Raça, data de nascimento, peso e observações são opcionais.

#### Scenario: Cadastro com os dados mínimos

- **WHEN** um tutor autenticado envia nome e espécie
- **THEN** o animal é criado e passa a aparecer na lista dele

#### Scenario: Nome ausente

- **WHEN** o cadastro é enviado sem nome
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Espécie ausente

- **WHEN** o cadastro é enviado sem espécie
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Campos opcionais em branco

- **WHEN** o cadastro é enviado sem raça, nascimento, peso e observações
- **THEN** o animal é criado normalmente

### Requirement: O dono do animal vem do servidor

O tutor dono de um animal SHALL ser determinado a partir da credencial de quem
faz a requisição. Qualquer identificador de tutor presente no corpo ou na URL
MUST ser ignorado, em todos os verbos.

#### Scenario: Dono forjado na criação

- **WHEN** a requisição de criação inclui o identificador de outro tutor
- **THEN** o animal é criado para o tutor da credencial, não para o informado

#### Scenario: Tentativa de doar o animal na edição

- **WHEN** a requisição de edição inclui o identificador de outro tutor
- **THEN** o animal permanece com o tutor que já o possuía

#### Scenario: Conta sem ficha de tutor tenta cadastrar

- **WHEN** uma conta autenticada que não possui ficha de tutor tenta criar um
  animal
- **THEN** a operação é recusada com mensagem explícita sobre a própria conta
- **AND** nenhum animal é gravado

### Requirement: Todo animal pertence a um tutor existente

O sistema SHALL garantir que nenhum animal seja gravado sem um tutor existente
associado. Um animal sem dono válido MUST NOT aparecer em nenhuma listagem nem
ser alcançável por nenhuma operação do tutor.

#### Scenario: Gravação sem dono válido é impedida

- **WHEN** qualquer caminho tentar gravar um animal cujo tutor não exista
- **THEN** a gravação é recusada

#### Scenario: Animal órfão não aparece para ninguém

- **WHEN** existir um animal sem tutor válido na base
- **THEN** ele não aparece em nenhuma listagem nem é devolvido por nenhuma
  consulta por identificador

### Requirement: Listagem restrita ao dono

A listagem de animais SHALL conter exatamente os animais do tutor
correspondente à credencial, e nenhum outro.

#### Scenario: Dois tutores, duas listas

- **WHEN** dois tutores com animais cadastrados pedem a própria listagem
- **THEN** cada um recebe apenas os seus
- **AND** nenhum identificador ou dado do outro aparece na resposta

#### Scenario: Tutor sem animais

- **WHEN** um tutor sem animais pede a listagem
- **THEN** recebe uma lista vazia, não um erro

#### Scenario: Conta sem ficha de tutor

- **WHEN** uma conta autenticada sem ficha de tutor pede a listagem
- **THEN** recebe uma lista vazia, não um erro

#### Scenario: Resposta não carrega dados do tutor

- **WHEN** qualquer listagem de animais é devolvida
- **THEN** a resposta contém apenas campos do animal
- **AND** não contém documento, telefone, e-mail ou endereço de tutor, nem o
  identificador do tutor

### Requirement: Leitura por identificador restrita ao dono

A consulta de um animal por identificador SHALL devolver o animal apenas ao seu
dono. Para qualquer outro caso MUST responder que não foi encontrado.

#### Scenario: O próprio animal

- **WHEN** um tutor consulta um animal seu pelo identificador
- **THEN** recebe os dados do animal

#### Scenario: Animal de outro tutor

- **WHEN** um tutor consulta pelo identificador um animal de outro tutor
- **THEN** recebe a resposta de "não encontrado"

#### Scenario: Identificador inexistente

- **WHEN** um tutor consulta um identificador que não existe
- **THEN** recebe **a mesma** resposta do cenário anterior, sem permitir
  distinguir os dois casos

### Requirement: Edição restrita ao dono

A edição de um animal SHALL ser permitida apenas ao seu dono, e MUST responder
que não foi encontrado em qualquer outro caso — inclusive quando o animal
existir e pertencer a outra pessoa.

#### Scenario: Edita o próprio animal

- **WHEN** um tutor edita um animal seu
- **THEN** os dados são atualizados
- **AND** o animal continua aparecendo na listagem dele

#### Scenario: Edita animal de outro tutor

- **WHEN** um tutor tenta editar um animal de outro tutor
- **THEN** recebe a resposta de "não encontrado"
- **AND** o animal permanece inalterado

#### Scenario: Edição não apaga o que não foi enviado

- **WHEN** um animal com raça, peso e observações preenchidos é editado
- **THEN** os campos não mencionados na intenção da edição permanecem com os
  valores que tinham
- **AND** observações clínicas não são perdidas por omissão

### Requirement: Nenhuma operação sem credencial

Todas as operações sobre animais SHALL exigir credencial válida, e a recusa
MUST acontecer no backend.

#### Scenario: Requisição sem credencial

- **WHEN** qualquer operação sobre animais é feita sem credencial, fora da
  interface
- **THEN** o backend recusa a requisição
- **AND** nenhum dado é devolvido

#### Scenario: Credencial inválida

- **WHEN** qualquer operação é feita com uma credencial forjada ou vencida
- **THEN** o backend recusa a requisição

### Requirement: Entradas de busca e ordenação não alteram o filtro de dono

Quando a listagem aceitar busca ou ordenação, esses valores SHALL ser
interpretados pelo servidor. Expressões recebidas do cliente MUST NOT
participar da condição que determina o dono.

#### Scenario: Valor de busca não escapa para a condição de dono

- **WHEN** a listagem recebe um valor de busca construído para alterar a
  condição da consulta
- **THEN** ele é tratado como texto a procurar
- **AND** a listagem continua restrita aos animais do tutor
