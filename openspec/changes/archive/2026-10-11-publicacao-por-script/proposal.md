## Why

Publicar no Xano hoje é um procedimento manual, registrado no design da
change `agendamento`: puxar o workspace numa pasta temporária, traduzir cada
arquivo do repositório (`apis/pet_bits/equipe_pedido_situacao.xs`) para o nome
que o Xano CLI espera (`api/pet_bits/equipe/pedidos/pedido_id/situacao_POST.xs`),
rodar o `--dry-run` com cada arquivo nomeado e só então publicar. A tradução à
mão já quase republicou o `entrar POST` sem querer, e se repete a cada change.

## What Changes

- Script `scripts/publicar.py <arquivos…>`:
  - deduz o caminho do CLI **lendo o arquivo** (`table`, `function`,
    `query … verb=` e o `api_group`), sem tabela mantida à mão;
  - valida os arquivos com o parser oficial antes de tudo;
  - puxa o workspace numa pasta temporária nova, copia por cima **só** os
    arquivos pedidos e roda o `--dry-run` com cada um nomeado;
  - só publica com `--publicar`, e mostra de novo o que vai mudar.
- `scripts/publicar.py --conferir`: traduz todos os `.xs` do repositório e
  compara com o workspace puxado, listando o que está no repositório e não no
  Xano (e o contrário). Detecta as divergências que hoje só aparecem por
  acaso.

## Capabilities

### New Capabilities

- `publicacao`: como o código do repositório chega ao Xano.

### Modified Capabilities

Nenhuma.

## Fora do escopo

- Publicar o repositório inteiro, ou apagar objetos no Xano: o script nunca
  usa `--sync` nem `--delete`.
- Publicação automática a cada push.

## Impact

- Código: `scripts/publicar.py`; `README.md`.
- O procedimento do registro da change `agendamento` passa a ser este
  script.
