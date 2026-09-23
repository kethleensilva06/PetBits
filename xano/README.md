# Backend do PetBits em XanoScript

Estes 54 arquivos `.xs` descrevem o backend do PetBits: as 9 tabelas e os 45
endpoints CRUD que o frontend Reflex consome. Eles existem para você não ter
que criar tabela por tabela e campo por campo no painel do Xano.

```
xano/
├── tables/            9 tabelas
└── apis/pet_bits/     45 endpoints (5 por tabela)
```

O API group deste projeto já existe no Xano e se chama **PetBits**:

```
https://x8ki-letl-twmt.n7.xano.io/api:Xj7KkS4w
```

Esse endereço já está no `.env` da raiz. A pasta é `pet_bits` porque a
extensão usa o nome do grupo em `snake_case` para nomear o diretório, e cada
query declara `api_group = "PetBits"` — assim o push cai nesse grupo, e não em
um novo.

Os nomes de tabela, de campo e os caminhos dos endpoints são exatamente os que
`petbits/xano.py` espera. Se você alterar algo aqui, altere também lá.

Todos os arquivos foram validados com o parser oficial do Xano (o que vem
embutido na extensão `xano.xanoscript`).

## Como enviar para o Xano

Você precisa fazer o login — eu não tenho como entrar na sua conta.

1. Instale a extensão (já instalada nesta máquina):
   `xano.xanoscript`
2. No VS Code, abra a paleta de comandos (`Ctrl+Shift+P`) e rode
   **Xano: Sign Up for Xano** (se ainda não tem conta) ou
   **Xano: Login to Xano**.
3. Rode **Xano: Select instance** e depois **Xano: Select workspace**.
4. A extensão cria o arquivo `.xano/config.json`. Nele há uma seção `paths`
   com as pastas onde ela procura cada tipo de objeto (`tables`, `apis`,
   `functions`, `tasks`, ...). Faça uma das duas coisas:
   - aponte `paths.tables` para `xano/tables` e `paths.apis` para `xano/apis`; **ou**
   - mova as pastas `tables/` e `apis/` de dentro de `xano/` para onde o
     `config.json` estiver apontando.
5. Rode **Xano: stage all changed files** e depois
   **Xano: Push Stage Changes to Xano**.

A pasta `apis/petbits/` é o que define o API group: no XanoScript, criar uma
pasta sob `apis/` cria um API group com aquele nome.

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
