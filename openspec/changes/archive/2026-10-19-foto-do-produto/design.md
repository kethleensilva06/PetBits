## Context

A change `perfil-e-fotos` montou o caminho inteiro de foto para o tutor e o
animal, e mediu o que o Xano faz: `storage.create_image` exige a extensão no
`filename` (sem ela, 500 "Invalid file extension."); o nome original do
arquivo não chega pelo `input`, então a extensão vem num campo `extensao` de
lista fechada, conferida com `|in:` (o `|contains:` é de texto e recusava até
o WebP); conteúdo que não é imagem faz o `create_image` lançar, e um
`try_catch` transforma isso em 400; `mime` e `size` só são conhecidos depois
de guardar. Do lado do Reflex, `rx.upload` com `accept`/`max_size` fazia o
arquivo recusado sumir sem aviso, então a conferência rápida mora em
`petbits/fotos_enviadas.py`.

Do lado do catálogo, `produto` não tem coluna de dono: a única recusa de
escrita é `PetBits/exige_equipe` em todo `equipe_produto_*`, e
`scripts/verificar_equipe.py` confere que ela está lá, antes do primeiro
`db.*`. Hoje a loja escolhe a imagem só no Reflex, por `imagem_do_produto`
em `petbits/ilustracoes.py`.

## Goals / Non-Goals

**Goals:** a equipe põe e troca a foto de qualquer produto pela tela, e a
loja passa a mostrá-la, sem requisição a mais em nenhuma das duas telas.

**Non-Goals:** apagar a foto, várias fotos, foto no cadastro antes de
salvar, imagem no balcão.

## Decisions

### D1. `image? foto` em `produto`

Coluna opcional, como em `tutor` e `pet`. Antes do push, `--dry-run` para
conferir que a única mudança na tabela é `ADD_FIELD foto`.

### D2. `POST equipe/produtos/{produto_id}/foto`, no molde do `pet/{pet_id}/foto`

Arquivo `apis/pet_bits/equipe_produto_foto.xs`, para cair no
`GLOB_EQUIPE` da guarda. Ordem da pilha, cada passo antes do que custa mais:

1. `precondition ($auth.id > 0)` e `function.run "PetBits/exige_equipe"` —
   a abertura de todo `equipe_*`, antes de qualquer `db.*`;
2. foto presente;
3. o produto existe (`db.query` por id, `output = ["id"]`) — **antes** de
   guardar, para um id errado não deixar arquivo órfão;
4. `extensao` na lista fechada `["jpg", "jpeg", "png", "webp"]` com `|in:`;
5. `storage.create_image` com `access = "public"` e
   `filename = "produto." ~ $input.extensao`, dentro de `try_catch` → 400;
6. `mime` na lista e `size <= 5242880`;
7. `db.patch produto` pelo id da consulta do passo 3, só com `{foto: ...}`.

Sem transação com trava, ao contrário do animal: lá a trava protege a posse
(o animal pode mudar de dono entre a prévia e a gravação); aqui não há dono,
e produto não é apagado (desativar é `ativo = false`), então o id do passo 3
continua válido.

Recusa de cliente sai pelo `exige_equipe`: 403 "Sem permissao para esta
area.", igual ao resto do catálogo, antes de o arquivo ser guardado.

### D3. A foto vai junto nas listas que já existem

`GET loja/produtos` e `GET equipe/produtos` ganham `foto` no `output`. Nenhuma
das telas faz requisição a mais: a imagem chega com a lista. O detalhe da
loja continua sem requisição, porque usa o item da lista.

### D4. Uma função decide a imagem, e as duas telas a usam

`imagem_do_produto(nome, categoria, foto=None)` em `petbits/ilustracoes.py`
passa a receber a foto do registro: com `foto.url`, devolve a URL; sem ela,
a regra de hoje. `LojaState.carregar_loja` e `EquipeState.carregar_produtos`
chamam a mesma função, então a equipe vê no cartão exatamente a imagem que o
cliente vê — e descobre ali qual produto ainda está com a foto da categoria.

### D5. Foto no diálogo de edição, como no animal

O diálogo de `/equipe/produtos` ganha, só na edição, a imagem atual e o
botão "Escolher foto"/"Trocar foto" (`rx.upload` sem `accept`/`max_size`),
com a conferência de `fotos_enviadas.extensao_da_foto` e o aviso em
vermelho. No cadastro aparece o texto "Depois de cadastrar, edite o produto
para pôr a foto dele.". A resposta do envio atualiza o item da lista na
hora, sem recarregar o catálogo (uma requisição a menos).

### D6. Acesso `public`, como no D3 da `perfil-e-fotos`

Foto de produto é vitrine: nada nela é privado. URL pública evita uma
requisição de assinatura por cartão.

## Risks / Trade-offs

- [Imagem guardada e recusada depois, por `mime` ou tamanho, fica órfã no
  armazenamento] → mesmo risco aceito na `perfil-e-fotos`: raro, pequeno e
  sem ficha que aponte para ele.
- [A foto da URL pública do Xano conta no limite de 10 a cada 20 s?] → a
  `perfil-e-fotos` assumiu que não. A loja tem 15 produtos, então aqui isso
  importa mais: medir antes de ligar a loja (tarefa 1.1).
- [O plano gratuito do Xano marca a imagem] → **medido na aplicação:** o
  `storage.create_image` grava o arquivo com "Powered by Xano" no canto. A
  foto enviada fica pior que a que acompanha o app. Não é resolvido aqui:
  trocar de plano ou medir `storage.create_attachment` é decisão à parte, e
  atinge também tutor e animal.
- [Foto trocada continua com a antiga no cache do navegador] → cada envio
  gera um caminho novo no armazenamento, então a URL muda junto.

## Verificação

- `node scripts/validar_xanoscript.mjs` nos `.xs` mexidos;
  `scripts/publicar.py` sem `--publicar` (prévia) antes de cada publicação,
  conferindo que a tabela só ganha a coluna.
- Contra o Xano, com conta de equipe: WebP aceito e `foto.url` na
  `equipe/produtos` e na `loja/produtos`; troca por PNG muda a URL; PDF →
  400 pela extensão; `.jpg` que não é imagem → 400; PNG > 5 MB → 400;
  `produto_id` inexistente → 404. Com conta de cliente: 403, e o produto
  continua com a foto de antes.
- `python scripts/verificar_equipe.py` — o endpoint novo entra na guarda.
- Navegador: como equipe, enviar foto da "Escova removedora de pelos" pelo
  diálogo, ver no cartão; como cliente, ver na loja e no detalhe; produto
  sem foto enviada continua com a de antes. Claro, escuro e celular.
- `python -m unittest`, com teste da ordem de escolha em
  `tests/test_ilustracoes.py`; `openspec validate foto-do-produto --strict`.
