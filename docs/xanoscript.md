# Backend do PetBits em XanoScript

Estes 54 arquivos `.xs` descrevem o backend do PetBits: as 9 tabelas e os 45
endpoints CRUD que o frontend Reflex consome. Eles existem para você não ter
que criar tabela por tabela e campo por campo no painel do Xano.

Eles ficam nas pastas que a extensão usa, declaradas em `.xano/config.json`:

```
tables/             9 tabelas do PetBits (+ as que vieram do pull do Xano)
apis/pet_bits/      45 endpoints (5 por tabela) + api_group.xs
```

> **Atenção:** os caminhos vêm de `.xano/config.json` (`paths.tables` e
> `paths.apis`). Se esses valores mudarem, os arquivos precisam acompanhar —
> a extensão só enxerga o que estiver nos caminhos configurados.

O API group deste projeto já existe no Xano e se chama **PetBits**:

```
https://x8ki-letl-twmt.n7.xano.io/api:Xj7KkS4w
```

Esse endereço já está no `.env` da raiz. A pasta é `pet_bits` porque a
extensão usa o nome do grupo em `snake_case` para nomear o diretório;
`apis/pet_bits/api_group.xs` declara o `canonical = "Xj7KkS4w"` e cada query
declara `api_group = "PetBits"` — assim o push cai nesse grupo, e não em um
novo.

As outras pastas na raiz (`functions/`, `tasks/`, `addons/`, `agents/`,
`mcp_servers/`, `middlewares/`) e os arquivos de `tables/` e `apis/` com
prefixo numérico (`770882_user.xs`, `apis/authentication/`, ...) vieram do
pull do workspace e **não fazem parte do PetBits** — não mexa neles.

Os nomes de tabela, de campo e os caminhos dos endpoints são exatamente os que
`petbits/xano.py` espera. Se você alterar algo aqui, altere também lá.

Todos os arquivos foram validados com o parser oficial do Xano (o que vem
embutido na extensão `xano.xanoscript`).

## Como enviar para o Xano

O push só pode ser feito de dentro do VS Code: ele depende das ferramentas da
extensão `xano.xanoscript`, que exigem a sua sessão autenticada no Xano.

A extensão já está instalada e o login já foi feito (`.xano/config.json`
aponta para a instância `x8ki-letl-twmt`, workspace `Kethleen's Workspace`,
branch `v1`). Falta só publicar:

1. `Ctrl+Shift+P` → **Xano: stage all changed files**
2. `Ctrl+Shift+P` → **Xano: Push Stage Changes to Xano**

Se preferir, o Copilot em modo Agent dentro do VS Code também consegue fazer o
push, porque é lá que as ferramentas `xano.xanoscript/*` ficam disponíveis.

## Conferindo depois do push

Para saber se os endpoints chegaram ao grupo certo, peça a especificação
OpenAPI do grupo — ela lista tudo que existe nele:

```bash
curl -s "https://x8ki-letl-twmt.n7.xano.io/apispec:Xj7KkS4w?type=json"
```

Se o push funcionou, aparecem 45 caminhos. Se continuar em zero, o push
provavelmente criou um grupo novo em vez de usar o `PetBits` — nesse caso
confira em **API** se surgiu um segundo grupo e, se surgiu, use o base URL
dele no `.env`.

Um teste direto de um endpoint:

```bash
curl -s "https://x8ki-letl-twmt.n7.xano.io/api:Xj7KkS4w/cliente"
```

| Resposta | Significado |
|---|---|
| `[]` ou uma lista JSON | funcionando |
| `Unable to locate request.` | o endpoint não existe: falta o push |
| `401` / `403` | o grupo exige token; preencha `XANO_TOKEN` no `.env` |

## O que cada endpoint faz

Para cada tabela `<t>`:

| Arquivo | Endpoint | Uso no frontend |
|---|---|---|
| `<t>_list.xs` | `GET /<t>` | `TabelaXano.listar()` |
| `<t>_get.xs` | `GET /<t>/{id}` | `TabelaXano.obter(id)` |
| `<t>_create.xs` | `POST /<t>` | `TabelaXano.criar(dados)` |
| `<t>_update.xs` | `PATCH /<t>/{id}` | `TabelaXano.atualizar(id, dados)` |
| `<t>_delete.xs` | `DELETE /<t>/{id}` | `TabelaXano.remover(id)` |

Duas decisões que valem registro:

- **O endpoint de edição substitui todos os campos que recebe.** Ele não faz
  merge com o registro existente: o campo que não vier na requisição é gravado
  como nulo. Isso é intencional — é o que permite limpar um campo opcional
  (apagar o e-mail de um cliente, por exemplo). Por isso o frontend sempre
  envia o registro completo no update. Se você criar outro cliente dessa API,
  siga a mesma regra.
- **A listagem já vem ordenada** (`nome` para cadastros, data decrescente para
  agendamentos, pedidos e prontuários), mas o frontend reordena por conta
  própria, porque isso não é garantido pelo CRUD do Xano.

## Diferenças em relação ao schema SQL original

O schema original (`Petshop_DQL`, SQL Server) usava recursos que o Xano não
tem. As adaptações:

| SQL Server | Xano |
|---|---|
| `id_cliente INT` como PK explícita | `id` gerado pelo Xano (PK de toda tabela) |
| `FOREIGN KEY` | campo `int` com `table = "<tabela>"` (vínculo declarado) |
| `CHECK (status IN (...))` | validado no frontend, a partir das constantes de `petbits/models.py` |
| `UNIQUE (cpf)` | índice `btree\|unique` sobre `cpf` |
| `ON DELETE CASCADE` | remoção explícita: excluir um pedido apaga antes os seus itens |
| `DEFAULT GETDATE()` | `timestamp <campo>?=now` |
