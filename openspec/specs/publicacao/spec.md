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
