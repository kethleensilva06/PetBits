## MODIFIED Requirements

### Requirement: Ilustrações sem custo de requisição

As imagens da área do cliente SHALL ser fotografias de licença livre,
guardadas como arquivos do próprio app e servidas com ele, cada uma com
origem e autor registrados em `assets/fotos/CREDITOS.md`. Escolher e mostrar
uma imagem SHALL NOT disparar requisição ao Xano nem a serviço externo.

#### Scenario: Abrir a loja

- **WHEN** a tutora abre a loja
- **THEN** as requisições ao Xano são as mesmas de antes, e as imagens vêm de `/fotos/`

#### Scenario: Toda foto tem crédito

- **WHEN** alguém confere `assets/fotos/`
- **THEN** cada arquivo de imagem tem uma linha em `CREDITOS.md` com a origem, o autor e a licença

#### Scenario: Foto não distorce

- **WHEN** uma foto aparece num lugar com proporção diferente da original
- **THEN** ela é recortada para caber, sem esticar

### Requirement: Imagem do produto pela categoria

Cada produto da loja SHALL mostrar a foto do próprio produto quando ela
existir — escolhida pelo nome e pela descrição, e encontrada pela chave do
nome —, e a foto da sua categoria quando não existir. Produto sem categoria
conhecida SHALL mostrar a foto genérica.

#### Scenario: Produto de higiene

- **WHEN** a loja lista a "Areia higiênica", da categoria `higiene`
- **THEN** o cartão mostra a foto de areia para gatos, e não a foto geral de higiene

#### Scenario: Produto novo sem foto própria

- **WHEN** a equipe cadastra um produto da categoria `acessorio` que ainda não tem foto
- **THEN** o cartão mostra a foto da categoria Acessório

#### Scenario: Categoria ausente

- **WHEN** um produto sem foto própria chega sem categoria
- **THEN** o cartão mostra a foto genérica
