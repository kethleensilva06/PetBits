# Backend do PetBits em XanoScript

Estes arquivos `.xs` descrevem o backend do PetBits: as 9 tabelas, os 45
endpoints CRUD que o frontend Reflex consome, o cadastro público de tutor e a
função de autorização que todos eles usam. Eles existem para você não ter que
criar tabela por tabela e campo por campo no painel do Xano.

Eles ficam nas pastas que a extensão usa, declaradas em `.xano/config.json`:

```
tables/             9 tabelas do PetBits (+ as que vieram do pull do Xano)
apis/pet_bits/      45 endpoints CRUD + cliente_signup + me_cliente + api_group.xs
functions/pet_bits/ ctx.xs -- a autorização que os 45 endpoints consultam
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
embutido na extensão `xano.xanoscript`). Para validar todos de uma vez, antes
de empurrar:

```bash
node scripts/validar_xanoscript.mjs apis/pet_bits/*.xs functions/pet_bits/*.xs tables/*.xs
```

Vale o hábito: o push é irreversível — um arquivo com erro de sintaxe
substitui um endpoint que funcionava. A extensão só valida o arquivo aberto.

Uma pegadinha que esse validador pega e é fácil de escrever errado: o `else`
do `conditional` precisa ficar **em linha própria**. `} else {` é erro de
sintaxe no XanoScript.

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
| `401` | sem token, ou token vencido: todos os endpoints exigem login |
| `403` | logado, mas sem direito àquilo — veja a seção de autorização |

## Autorização

**Todos os 45 endpoints exigem login** (`auth = "user"`). As duas únicas
exceções são propositais: `POST /cliente/signup`, que é a porta de entrada, e
`POST /auth/login`, que fica no grupo Authentication.

Quem decide o que cada pessoa pode é `functions/pet_bits/ctx.xs`. Ele recebe o
`$auth.id` e devolve `{user_id, role, is_admin, cliente_id}`:

```
function.run "PetBits/ctx" {
  input = {user_id: $auth.id}
} as $ctx
```

Três decisões que valem explicar:

- **O papel vem sempre do banco, nunca do token.** O `auth/login` do template
  cria o token com `extras = {}`, e é assim que fica. Papel dentro do token
  congelaria por 24 horas: rebaixar um administrador não teria efeito até o
  token vencer.
- **`ctx` falha fechada.** Um login sem ficha de cliente correspondente recebe
  `accessdenied` em vez de `cliente_id` nulo. Isso importa porque um filtro que
  ignora valor nulo devolveria a tabela inteira justamente para quem não
  deveria ver nada.
- **O papel guardado no navegador não protege coisa nenhuma.** Ele serve para
  esconder botão; qualquer pessoa edita o `localStorage` pelo DevTools. Quem
  barra é este arquivo.

### O que cada papel alcança

| Tabela | list | get | create | update | delete |
|---|---|---|---|---|---|
| produto, servico | logado | logado | clínica | clínica | clínica |
| funcionario | logado¹ | logado¹ | clínica | clínica | clínica |
| cliente | clínica | clínica | clínica | clínica | clínica |
| pet | só os seus | só os seus | dono forçado² | só os seus³ | clínica |
| pedido | só os seus | só os seus | clínica | clínica | clínica |
| agendamento | só os seus⁴ | só os seus⁴ | pet seu, `agendado`⁵ | só cancelar⁶ | clínica |
| prontuario | só os seus⁴ | só os seus⁴ | clínica | clínica | clínica |
| itens_pedido | só os seus⁴ | só os seus⁴ | clínica | clínica | clínica |

1. O tutor recebe só `id`, `nome` e `cargo`. Ele precisa do nome de quem
   atendeu (aparece no histórico), mas a ficha tem CPF, telefone e e-mail.
2. O `dblink` transforma **toda** coluna da tabela em entrada, inclusive
   `id_cliente`. Para o tutor esse valor é ignorado e trocado pela ficha dele;
   sem isso bastaria mandar outro id para cadastrar um pet na conta alheia.
3. `id_cliente` e `id` saem do corpo antes de gravar. O `filter_null` não
   serve para isso: ele descarta nulo, não um inteiro forjado.
4. O dono está a um salto (no `pet` ou no `pedido`). O filtro entra como
   `join`, para o recorte acontecer no banco em vez de depois de baixar a
   tabela inteira.
5. O status sai sempre como `"agendado"`; deixar o corpo escolher permitiria
   gravar uma consulta já como concluída.
6. O corpo do tutor é descartado inteiro em favor de `{status: "cancelado"}`.
   Senão ele remarcaria por cima de um horário ocupado, ou passaria a consulta
   para outro pet.

Excluir é sempre da clínica, inclusive nas tabelas com dono: apagar um pet
deixaria prontuários e agendamentos apontando para o vazio, e o tutor tem o
cancelamento para o que de fato precisa desfazer.

### Virar administradora

O cadastro pelo site cria sempre `role: "member"` — é isso que permite ele ser
público. Promover acontece fora da aplicação:

```bash
python scripts/promover_admin.py voce@email.com
```

Ou, sem script nenhum: painel do Xano → Database → tabela `user` → sua linha →
trocar `role` para `admin`. A coluna é `private`, o que a esconde da API, não
do painel.

### Conferindo

O teste que decide se a autorização vale é `curl`, não a tela:

```bash
curl -s -o /dev/null -w "%{http_code}
" https://x8ki-letl-twmt.n7.xano.io/api:Xj7KkS4w/cliente
```

Tem que responder `401`. Com um token de tutor, `DELETE /funcionario/1`
responde `403`, e `GET /pet` traz só os pets dele.

## O que cada endpoint faz

Para cada tabela `<t>`:

| Arquivo | Endpoint | Uso no frontend |
|---|---|---|
| `<t>_list.xs` | `GET /<t>` | `TabelaXano.listar()` |
| `<t>_get.xs` | `GET /<t>/{id}` | `TabelaXano.obter(id)` |
| `<t>_create.xs` | `POST /<t>` | `TabelaXano.criar(dados)` |
| `<t>_update.xs` | `PATCH /<t>/{id}` | `TabelaXano.atualizar(id, dados)` |
| `<t>_delete.xs` | `DELETE /<t>/{id}` | `TabelaXano.remover(id)` |

Mais dois, fora do CRUD:

| Arquivo | Endpoint | Uso |
|---|---|---|
| `cliente_signup.xs` | `POST /cliente/signup` | cadastro público do tutor: cria `user` + `cliente` vinculados e devolve o token |
| `me_cliente.xs` | `GET /me/cliente` | a ficha de cliente de quem está logado |

Os endpoints de escrita (`_create` e `_update`) seguem o padrão que o próprio
Xano gera: o bloco `input` usa `dblink { table = "..." }` em vez de listar
campo a campo. Isso importa por três motivos, todos verificados contra a API:

- **Campos `date` não aceitam `null` quando listados manualmente.** Com o
  `input` campo a campo, enviar `data_nascimento: null` — ou omitir a chave —
  devolvia `500 Unable to locate input: data_nascimento`. Com `dblink`
  funciona. Afetava `funcionario`, `pet` e `prontuario`.
- **O update exige o registro completo.** O `dblink` transforma os campos
  obrigatórios da tabela em inputs obrigatórios, então um PATCH parcial devolve
  `400 Missing param: <campo>`. O frontend sempre envia o registro inteiro; se
  você chamar essa API de outro lugar, faça o mesmo. `PedidoState`, por
  exemplo, lê o pedido antes de regravar o `valor_total`.
- **Nulos viram o default do tipo.** Texto vira `""` e decimal vira `0` — não
  ficam nulos. Os States tratam isso na exibição (`valor or "-"`), então a
  interface mostra `-` do mesmo jeito.

A rota do update usa `{<tabela>_id}` em vez de `{id}` (ex.:
`PATCH /cliente/{cliente_id}`), porque o `dblink` já expõe um input `id` vindo
do schema e dois inputs com o mesmo nome colidiriam. A URL chamada continua
sendo `/cliente/5`, então o cliente HTTP não muda.

**A listagem já vem ordenada** (`nome` para cadastros, data decrescente para
agendamentos, pedidos e prontuários), mas o frontend reordena por conta
própria, porque isso não é garantido pelo CRUD do Xano.

**Limite do plano gratuito:** 10 requisições a cada 20 segundos. O painel
sozinho consulta sete tabelas, então `petbits/xano.py` controla o ritmo com uma
janela deslizante e tenta de novo quando o Xano devolve 429.

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
