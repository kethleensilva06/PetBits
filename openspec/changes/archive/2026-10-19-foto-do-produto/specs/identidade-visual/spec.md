## MODIFIED Requirements

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
