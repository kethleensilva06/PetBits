## ADDED Requirements

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
