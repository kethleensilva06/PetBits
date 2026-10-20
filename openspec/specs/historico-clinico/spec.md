# historico-clinico Specification

## Purpose
Define o Atendimento — o prontuário, no vocabulário da clínica —, que preserva o
histórico clínico de cada animal: quem registra (a equipe), quem lê (a equipe e o
tutor do animal) e a regra que o torna a memória do sistema: um atendimento não
se altera nem se apaga; corrige-se por retificação.

## Requirements

### Requirement: A equipe registra o atendimento

Uma conta de equipe SHALL registrar um atendimento de um animal informando o
colaborador que atendeu, a data e o diagnóstico; motivo, tratamento, peso e
data de retorno são opcionais. O colaborador MUST estar ativo e ser
veterinário ou clínico geral. A data MUST NOT ser no futuro, e o retorno,
quando houver, MUST NOT ser antes da data. O backend SHALL guardar quem
registrou, pela conta do token.

#### Scenario: Atendimento de emergência

- **WHEN** a equipe registra, pela lista de animais, uma consulta da Mel com a Dra. Leticia e o diagnóstico "Otite"
- **THEN** o atendimento passa a existir no histórico da Mel

#### Scenario: Diagnóstico em branco

- **WHEN** o diagnóstico vai em branco
- **THEN** o registro é recusado com o motivo

#### Scenario: Quem atendeu não é da área clínica

- **WHEN** o colaborador escolhido é tosador, atendente ou está desligado
- **THEN** o registro é recusado

#### Scenario: Conta de tutor tenta registrar

- **WHEN** uma conta de tutor chama o registro, fora da interface
- **THEN** o backend recusa e nada é gravado

### Requirement: O histórico não se apaga nem se edita

Um atendimento registrado MUST NOT ser alterado nem removido. Corrigir SHALL
ser registrar uma retificação: um atendimento novo, do mesmo animal, que
aponta para o corrigido. O corrigido SHALL continuar no histórico, marcado
como retificado.

#### Scenario: Retificar um diagnóstico

- **WHEN** a equipe retifica o atendimento de "Otite" com o diagnóstico "Otite externa bilateral"
- **THEN** o histórico mostra os dois, o primeiro marcado como retificado e o novo como retificação dele

#### Scenario: Retificar atendimento de outro animal

- **WHEN** a retificação aponta para um atendimento de outro animal
- **THEN** é recusada

#### Scenario: Não há como apagar

- **WHEN** alguém procura alterar ou remover um atendimento
- **THEN** não existe endpoint para isso

### Requirement: O tutor lê o histórico dos seus animais

O tutor SHALL ler o histórico de cada animal dele, do mais recente para o
mais antigo, com data, motivo, diagnóstico, tratamento, peso, retorno e o
nome e a função de quem atendeu. O contato do colaborador MUST NOT ser
devolvido. Animal de outro tutor SHALL ter a mesma resposta de animal
inexistente.

#### Scenario: Linha do tempo da Mel

- **WHEN** a tutora abre o histórico da Mel
- **THEN** vê os atendimentos dela, o mais recente primeiro, com quem atendeu

#### Scenario: Animal de outro tutor

- **WHEN** alguém pede o histórico de um animal que não é seu
- **THEN** a resposta é a de animal não encontrado, sem dado nenhum

#### Scenario: Sem atendimento ainda

- **WHEN** o animal não tem atendimento
- **THEN** a tela diz que ainda não há registro

### Requirement: Evolução do peso

O histórico de um animal SHALL mostrar o último peso registrado, com a data,
a diferença para a pesagem anterior e as últimas seis pesagens, para a equipe
e para o tutor. Atendimento retificado MUST NOT entrar na conta. Sem nenhuma
pesagem, o quadro SHALL NOT aparecer.

#### Scenario: Engordou

- **WHEN** a Mel pesou 28 kg em setembro e 28,5 kg em outubro
- **THEN** o histórico mostra "28,5 kg" e "+0,5 kg desde" a data de setembro

#### Scenario: Peso corrigido

- **WHEN** o atendimento de outubro foi retificado com 28,2 kg
- **THEN** o histórico usa 28,2 kg, e não o peso do registro retificado
