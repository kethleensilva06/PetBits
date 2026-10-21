# publicacao

## Purpose

Define como o código do repositório chega ao Xano: só os arquivos nomeados,
com prévia antes, publicação só quando pedida, e a conferência do repositório
inteiro contra o workspace.

## Requirements

### Requirement: Publicar só os arquivos pedidos, com prévia

O projeto SHALL ter um script que publica no Xano apenas os arquivos do
repositório que forem nomeados, deduzindo o caminho do Xano CLI pelo conteúdo
de cada arquivo. O script MUST validar os arquivos com o parser oficial, MUST
mostrar a prévia (`--dry-run`) antes de qualquer publicação e MUST publicar
só quando pedido explicitamente. O script MUST NOT usar `--sync` nem
`--delete`.

#### Scenario: Prévia

- **WHEN** quem desenvolve roda o script com dois arquivos e sem `--publicar`
- **THEN** vê o que mudaria no Xano para esses dois arquivos, e nada é
  publicado

#### Scenario: Arquivo inválido

- **WHEN** um dos arquivos não passa no parser oficial
- **THEN** o script para antes de puxar ou publicar qualquer coisa

#### Scenario: Caminho deduzido

- **WHEN** o arquivo é `apis/pet_bits/equipe_pedido_situacao.xs`, com
  `query "equipe/pedidos/{pedido_id}/situacao" verb=POST`
- **THEN** o caminho no CLI é
  `api/pet_bits/equipe/pedidos/pedido_id/situacao_POST.xs`

### Requirement: Conferir o repositório contra o Xano

O script SHALL comparar todos os `.xs` do repositório com o workspace puxado
do Xano e listar o que existe só num dos lados.

#### Scenario: Arquivo despublicado ainda no repositório

- **WHEN** um endpoint foi despublicado no Xano mas o `.xs` continua no
  repositório
- **THEN** a conferência o lista como "no repositório, não no Xano"

### Requirement: O repositório só guarda endpoints que estão no ar

Um `.xs` de endpoint que não está publicado no Xano MUST NOT ficar no
repositório: quando um endpoint sai do ar, o arquivo sai na mesma change.

#### Scenario: Endpoint despublicado

- **WHEN** um endpoint é despublicado no Xano
- **THEN** o `.xs` dele é removido do repositório na mesma change, e a
  guarda `verificar_equipe.py` não o acusa mais

### Requirement: Publicar o site sem segredo nem conta de teste

A publicação do site no Reflex Cloud SHALL mandar só os arquivos que o site
usa e só as variáveis `XANO_BASE_URL` e `XANO_AUTH_BASE_URL`. O `.env`, o
arquivo de contas de teste, o `XANO_META_TOKEN` e o export do Xano MUST NOT
ser enviados. Por padrão, a publicação SHALL só mostrar o plano, sem enviar
nada.

#### Scenario: Prévia

- **WHEN** alguém roda `scripts/publicar_no_reflex.py` sem `--publicar`
- **THEN** vê os arquivos que iriam e os nomes das variáveis, sem valores, e nada é enviado

#### Scenario: Arquivo proibido no pacote

- **WHEN** o arquivo de contas de teste entraria no pacote
- **THEN** o script para antes de chamar o `reflex deploy`

### Requirement: O site também no GitHub Pages

A parte visual do site SHALL poder ser publicada no GitHub Pages do repositório,
em https://kethleensilva06.github.io/PetBits/, ligada ao servidor do Reflex
Cloud. Abrir qualquer endereço do site direto SHALL funcionar, e as imagens do
app MUST carregar sob o prefixo `/PetBits/`. Nada do `.env` MUST ir para o
GitHub Pages.

#### Scenario: Abrir a loja direto

- **WHEN** alguém sem sessão abre https://kethleensilva06.github.io/PetBits/loja
- **THEN** o servidor do Reflex Cloud responde e leva à entrada de clientes

#### Scenario: Fotos da página inicial

- **WHEN** a página inicial abre no GitHub Pages
- **THEN** as fotos carregam de `/PetBits/fotos/`
