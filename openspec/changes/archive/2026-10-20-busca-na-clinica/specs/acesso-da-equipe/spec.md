## ADDED Requirements

### Requirement: As listas da clínica têm busca

As telas de colaboradores, tutores e animais da clínica SHALL ter um campo de
busca que filtra a lista já carregada, sem requisição ao backend, ignorando
maiúsculas e acentos e exigindo que todas as palavras digitadas apareçam. Nos
tutores, CPF e telefone SHALL ser encontrados também só pelos números.

#### Scenario: Buscar um animal pelo tutor

- **WHEN** alguém da equipe digita "ana mel" em Animais
- **THEN** a lista mostra só os animais chamados Mel da tutora Ana

#### Scenario: Buscar um tutor pelo CPF

- **WHEN** alguém da equipe digita "12345678" em Tutores
- **THEN** aparece o tutor de CPF 123.456.78x-xx

#### Scenario: Nada encontrado

- **WHEN** a busca não acha ninguém
- **THEN** a tela diz que nada foi encontrado para aquela busca, e não que a lista está vazia
