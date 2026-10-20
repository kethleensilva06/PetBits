# identidade-visual Specification

## Purpose
Define a aparência comum do PetBits — o tema, a marca e os cabeçalhos de
navegação da área do cliente e da área da clínica —, para que todas as telas
se reconheçam como o mesmo sistema e o topo não mude de lugar entre elas.

## Requirements

### Requirement: Tema do sistema

O app SHALL usar um tema único em todas as telas: cor principal verde-água
(`teal`), cinza quente (`sand`), cantos grandes e a fonte Nunito, sempre na
aparência clara, com o fundo da página branco. A aparência MUST NOT mudar
com a preferência do sistema operacional nem com escolha guardada no
navegador.

#### Scenario: Sistema em modo claro

- **WHEN** alguém abre qualquer tela com o sistema em modo claro
- **THEN** a tela aparece clara, com fundo branco, botões principais verde-água e texto em Nunito

#### Scenario: Sistema em modo escuro

- **WHEN** alguém abre qualquer tela com o sistema em modo escuro
- **THEN** a tela aparece clara do mesmo jeito, com fundo branco

#### Scenario: Trocar pelo ícone

- **WHEN** alguém procura o ícone de sol/lua no topo ou nas portas de entrada
- **THEN** não há ícone: a aparência não se troca pela tela

#### Scenario: A escolha fica

- **WHEN** o navegador guardou o escuro pelo ícone que existia antes
- **THEN** a tela abre clara mesmo assim, e o valor guardado passa a ser o claro

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

Cada produto da loja SHALL mostrar, nesta ordem: a foto enviada pela equipe,
quando houver; senão a foto do próprio produto que acompanha o app —
escolhida pelo nome e pela descrição, e encontrada pela chave do nome —;
senão a foto da sua categoria. Produto sem categoria conhecida SHALL mostrar
a foto genérica. A tela da equipe SHALL mostrar a mesma imagem que a loja
mostra.

#### Scenario: Produto de higiene

- **WHEN** a loja lista a "Areia higiênica", da categoria `higiene`, sem foto enviada
- **THEN** o cartão mostra a foto de areia para gatos, e não a foto geral de higiene

#### Scenario: Foto enviada pela equipe vence

- **WHEN** a equipe enviou uma foto para a "Areia higiênica"
- **THEN** o cartão e o detalhe da loja mostram a foto enviada, e não a que acompanha o app

#### Scenario: Produto novo sem foto própria

- **WHEN** a equipe cadastra um produto da categoria `acessorio` e não envia foto
- **THEN** o cartão mostra a foto da categoria Acessório

#### Scenario: Categoria ausente

- **WHEN** um produto sem foto chega sem categoria
- **THEN** o cartão mostra a foto genérica

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

As imagens que acompanham o app SHALL ser fotografias de licença livre,
guardadas como arquivos do próprio app e servidas com ele, cada uma com
origem e autor registrados em `assets/fotos/CREDITOS.md`. As fotos enviadas
por pessoas — do tutor, do animal e do produto — SHALL ficar no
armazenamento público do Xano e chegar à tela pela URL que vem junto com o
registro. Escolher e mostrar uma imagem SHALL NOT disparar requisição à API
do Xano além das que a tela já faz.

#### Scenario: Abrir a loja

- **WHEN** a tutora abre a loja
- **THEN** as requisições à API do Xano são as mesmas de antes; as imagens vêm de `/fotos/` ou da URL pública da foto enviada

#### Scenario: Toda foto tem crédito

- **WHEN** alguém confere `assets/fotos/`
- **THEN** cada arquivo de imagem tem uma linha em `CREDITOS.md` com a origem, o autor e a licença

#### Scenario: Foto não distorce

- **WHEN** uma foto aparece num lugar com proporção diferente da original
- **THEN** ela é recortada para caber, sem esticar

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

### Requirement: As abas do cliente têm a mesma largura

Meus animais, Agendar, Loja, Meus pedidos e Meu perfil SHALL ocupar a mesma
largura de página e começar no mesmo ponto da tela, tenha a aba barra de
rolagem ou não, para o cabeçalho, o avatar e o menu ficarem no mesmo lugar ao
trocar de aba.

#### Scenario: Da casa para a loja

- **WHEN** a tutora vai de Meus animais para a Loja numa tela larga
- **THEN** o conteúdo das duas ocupa a mesma largura, e o cabeçalho não muda de lugar

#### Scenario: Aba curta e aba longa

- **WHEN** Meus animais cabe na tela sem rolar e a Loja precisa de rolagem
- **THEN** o cabeçalho e o avatar ficam exatamente no mesmo lugar nas duas

### Requirement: Esqueletos enquanto a tela carrega

Enquanto os dados de uma tela não chegaram, a tela SHALL mostrar blocos
cinza no formato do conteúdo que vai aparecer, no lugar do spinner com
"Carregando...". O esqueleto MUST NOT aparecer junto com o conteúdo, com a
tela vazia nem com o erro, e SHALL avisar o leitor de tela de que a tela está
carregando.

#### Scenario: Abrir a loja

- **WHEN** a tutora abre a loja e os produtos ainda não chegaram
- **THEN** vê cartões cinza na grade dos produtos, e os produtos entram no lugar deles

#### Scenario: A carga falhou

- **WHEN** a carga de Meus pedidos falha
- **THEN** aparece o aviso de erro e nenhum esqueleto

#### Scenario: Leitor de tela

- **WHEN** um leitor de tela passa pelo esqueleto
- **THEN** ele lê que a tela está carregando
