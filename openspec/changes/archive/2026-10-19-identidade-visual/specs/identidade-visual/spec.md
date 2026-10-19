## ADDED Requirements

### Requirement: Tema do sistema

O app SHALL usar um tema único em todas as telas: cor principal verde-água
(`teal`), cinza quente (`sand`), cantos grandes e a fonte Nunito. A aparência
clara ou escura SHALL seguir a preferência do sistema operacional.

#### Scenario: Sistema em modo claro

- **WHEN** alguém abre qualquer tela com o sistema em modo claro
- **THEN** a tela aparece clara, com botões principais verde-água e texto em Nunito

#### Scenario: Sistema em modo escuro

- **WHEN** alguém abre qualquer tela com o sistema em modo escuro
- **THEN** a tela aparece escura, com a mesma cor principal

### Requirement: Marca do PetBits

A marca (selo com patinha e o nome PetBits) SHALL aparecer no topo das portas
de entrada, da área do cliente e da área da clínica. Nas áreas logadas, a
marca SHALL levar à tela inicial da área.

#### Scenario: Marca na área do cliente

- **WHEN** o tutor clica na marca em qualquer tela da área do cliente
- **THEN** vai para a casa (`/`)

#### Scenario: Marca na área da clínica

- **WHEN** alguém da equipe clica na marca em qualquer tela da clínica
- **THEN** vai para o painel (`/equipe`)

### Requirement: Cabeçalho da área do cliente

As telas da área do cliente (casa, agenda, loja e meus pedidos) SHALL ter o
mesmo cabeçalho, com os destinos Meus animais, Agendar, Loja e Meus pedidos,
a tela atual destacada, o papel da conta e o botão Sair. O cabeçalho SHALL
ser desenhado sem nenhuma requisição ao backend.

#### Scenario: Navegar entre as telas

- **WHEN** o tutor vai da casa para a loja pelo cabeçalho
- **THEN** o cabeçalho continua no mesmo lugar e passa a destacar Loja

#### Scenario: Cabeçalho não consulta o backend

- **WHEN** uma tela da área do cliente é aberta
- **THEN** as requisições ao Xano são as mesmas de antes desta change

### Requirement: Menu da área da clínica

As telas da clínica SHALL mostrar o menu das áreas como abas, com a área atual
destacada, abaixo de um topo com a marca, o nome de quem entrou, o papel e o
botão Sair.

#### Scenario: Área atual destacada

- **WHEN** alguém da equipe abre `/equipe/servicos`
- **THEN** a aba Serviços aparece destacada e as outras não
