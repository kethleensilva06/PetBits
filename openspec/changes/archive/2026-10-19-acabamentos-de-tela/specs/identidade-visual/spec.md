## ADDED Requirements

### Requirement: Mensagens em português correto

As recusas que o backend devolve sem acento SHALL chegar à tela acentuadas.
A acentuação MUST valer para todas as mensagens conhecidas dos endpoints do
PetBits, e uma mensagem desconhecida SHALL aparecer como veio.

#### Scenario: Senha atual errada

- **WHEN** o backend recusa com "A senha atual nao confere."
- **THEN** a tela mostra "A senha atual não confere."

#### Scenario: Frase que começa com "Esta"

- **WHEN** a recusa é "Esta conta nao tem ficha de tutor."
- **THEN** a tela mostra "Esta conta não tem ficha de tutor.", sem trocar o "Esta"

### Requirement: Menu da clínica no celular

Em tela estreita, o menu da área da clínica SHALL virar um botão que abre a
lista das áreas, mostrando a área atual, e o topo MUST caber numa linha.

#### Scenario: Abrir o menu no celular

- **WHEN** alguém da equipe, no celular, toca no botão do menu
- **THEN** vê as 9 áreas e vai para a que tocar

#### Scenario: Tela larga

- **WHEN** a tela é larga
- **THEN** as abas aparecem como antes, sem o botão

### Requirement: Avisos de sucesso passageiros

As confirmações de sucesso do perfil SHALL aparecer como notificação que some
sozinha, e não como texto parado na tela.

#### Scenario: Salvar os dados

- **WHEN** a pessoa salva os dados do perfil
- **THEN** aparece "Dados atualizados." numa notificação que some sozinha
