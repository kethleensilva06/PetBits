# identidade-visual Specification

## Purpose
Define a aparência comum do PetBits — o tema, a marca e os cabeçalhos de
navegação da área do cliente e da área da clínica —, para que todas as telas
se reconheçam como o mesmo sistema e o topo não mude de lugar entre elas.

## Requirements

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

### Requirement: Avatar do animal pela espécie

Cada cartão de animal na casa do cliente SHALL mostrar uma ilustração
escolhida pela espécie digitada: cão para "cão", "cachorro" ou "cadela", gato
para "gato" ou "gata", e uma ilustração genérica para qualquer outra coisa. A
escolha SHALL ignorar maiúsculas, acentos e espaços nas pontas.

#### Scenario: Espécie de cão escrita de vários jeitos

- **WHEN** o animal tem espécie "Cachorro", "cão" ou " CAO "
- **THEN** o cartão mostra a ilustração do cão

#### Scenario: Espécie desconhecida

- **WHEN** o animal tem espécie "Calopsita"
- **THEN** o cartão mostra a ilustração genérica, sem erro

### Requirement: Imagem do produto pela categoria

Cada produto da loja SHALL mostrar a ilustração da sua categoria. Produto sem
categoria conhecida SHALL mostrar uma ilustração genérica de sacola.

#### Scenario: Produto de higiene

- **WHEN** a loja lista um produto da categoria `higiene`
- **THEN** o cartão mostra a ilustração de higiene

#### Scenario: Categoria ausente

- **WHEN** um produto chega sem categoria
- **THEN** o cartão mostra a sacola genérica

### Requirement: Banner de boas-vindas da casa

A casa do cliente SHALL abrir com um banner que tem uma ilustração, a
saudação pelo nome e atalhos para Agendar e Loja.

#### Scenario: Atalho do banner

- **WHEN** a tutora clica em Agendar no banner
- **THEN** vai para `/agenda`

### Requirement: Telas vazias ilustradas

Quando a casa não tem animal, quando Meus pedidos não tem pedido e quando
Meus agendamentos não tem agendamento, a tela SHALL mostrar uma ilustração,
um texto que diga o que fazer e um botão para fazê-lo. Enquanto a lista
carrega ou quando ela falhou, a tela vazia SHALL NOT aparecer.

#### Scenario: Sem pedidos

- **WHEN** a tutora abre Meus pedidos e não tem nenhum
- **THEN** vê a ilustração, o texto e um botão que leva à Loja

#### Scenario: Ainda carregando

- **WHEN** a lista de pedidos ainda não chegou
- **THEN** aparece o carregando, não a tela vazia

### Requirement: Ilustrações sem custo de requisição

As ilustrações SHALL ser arquivos do próprio app, servidos com ele. Escolher
e mostrar uma ilustração SHALL NOT disparar requisição ao Xano nem a
serviço externo.

#### Scenario: Abrir a loja

- **WHEN** a tutora abre a loja
- **THEN** as requisições ao Xano são as mesmas de antes desta change, e as imagens vêm de `/ilustracoes/`
