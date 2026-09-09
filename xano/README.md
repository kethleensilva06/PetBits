# Backend do PetBits em XanoScript

Estes 54 arquivos `.xs` descrevem o backend do PetBits: as 9 tabelas e os 45
endpoints CRUD que o frontend Reflex consome. Eles existem para você não ter
que criar tabela por tabela e campo por campo no painel do Xano.

```
xano/
├── tables/            9 tabelas
└── apis/petbits/      45 endpoints (5 por tabela)
```

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

## Pegando a URL da API

Depois do push, o Xano gera o endereço do API group. Ele tem este formato:

```
https://<workspace>.<regiao>.xano.io/api:<canonical>
```

O `<canonical>` é um identificador curto e aleatório (algo como `HZ4jLtdc`)
que **o Xano gera** — não é possível saber ou escolher antes de o grupo
existir. Copie o endereço no painel do Xano, na tela do API group, e cole no
`.env` da raiz do projeto:

```
XANO_BASE_URL=https://x8ki-letl-twmt.n7.xano.io/api:HZ4jLtdc
XANO_TOKEN=
```

Se quiser fixar o canonical em vez de aceitar o gerado, o XanoScript permite
declarar as configurações do grupo:

```xs
api_group petbits {
  description = "Endpoints CRUD do PetBits"
  canonical = "HZ4jLtdc"
}
```

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
