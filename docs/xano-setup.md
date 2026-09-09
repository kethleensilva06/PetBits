# Configurar o Xano para o PetBits

O banco de dados do PetBits fica hospedado no [Xano](https://xano.com). A
aplicação Reflex não tem banco local: ela conversa com o Xano por HTTP através
de `petbits/xano.py`.

Este documento descreve o que precisa existir no Xano para a aplicação
funcionar.

> **Caminho rápido:** as tabelas e os endpoints já estão escritos em
> XanoScript na pasta [`xano/`](../xano/README.md). Se você usar a extensão
> `xano.xanoscript` no VS Code, basta fazer login e dar push — não precisa
> criar nada à mão. As seções abaixo descrevem a estrutura para quem preferir
> montar pelo painel do Xano, e servem como referência do que os arquivos
> `.xs` definem.

## 1. Criar o workspace e as tabelas

No painel do Xano, crie uma tabela para cada entidade abaixo. Os nomes das
tabelas e dos campos precisam ser **exatamente** estes — o cliente HTTP monta
as URLs a partir do nome da tabela e envia o JSON com estes nomes de campo.

O Xano cria sozinho, em toda tabela, os campos `id` e `created_at`. Não os
declare e não os envie na escrita.

### cliente

| Campo | Tipo no Xano |
|---|---|
| `nome` | text |
| `cpf` | text |
| `email` | text |
| `telefone` | text |
| `endereco` | text |
| `data_cadastro` | timestamp |

### funcionario

| Campo | Tipo no Xano |
|---|---|
| `nome` | text |
| `cpf` | text |
| `cargo` | text |
| `telefone` | text |
| `email` | text |
| `data_contratacao` | date |

`cargo` aceita `veterinario`, `tosador` ou `atendente`.

### produto

| Campo | Tipo no Xano |
|---|---|
| `nome` | text |
| `categoria` | text |
| `marca` | text |
| `unidade` | text |
| `preco_venda` | decimal |

### servico

| Campo | Tipo no Xano |
|---|---|
| `nome_servico` | text |
| `descricao` | text |
| `preco` | decimal |
| `duracao_estimada` | int |

### pet

| Campo | Tipo no Xano |
|---|---|
| `id_cliente` | int |
| `nome` | text |
| `especie` | text |
| `raca` | text |
| `data_nascimento` | date |
| `peso` | decimal |
| `observacoes` | text |

### pedido

| Campo | Tipo no Xano |
|---|---|
| `id_cliente` | int |
| `data_pedido` | timestamp |
| `status` | text |
| `valor_total` | decimal |

`status` aceita `pendente`, `pago`, `enviado` ou `entregue`.

### agendamento

| Campo | Tipo no Xano |
|---|---|
| `id_pet` | int |
| `id_servico` | int |
| `id_funcionario` | int |
| `data_hora` | timestamp |
| `status` | text |
| `observacoes` | text |

`status` aceita `agendado`, `em_andamento`, `concluido` ou `cancelado`.

### itens_pedido

| Campo | Tipo no Xano |
|---|---|
| `id_pedido` | int |
| `id_produto` | int |
| `quantidade` | int |
| `valor_unitario` | decimal |
| `valor_total` | decimal |

### prontuario

| Campo | Tipo no Xano |
|---|---|
| `id_pet` | int |
| `id_funcionario` | int |
| `data_atendimento` | timestamp |
| `diagnostico` | text |
| `tratamento_realizado` | text |
| `proxima_consulta` | date |

### Sobre os campos `id_*`

No SQL Server original esses campos eram chaves estrangeiras. Aqui eles são
inteiros simples que guardam o `id` do registro relacionado. Se preferir, o
Xano permite declará-los como `table reference` — o valor trafega como inteiro
do mesmo jeito, então a aplicação funciona nas duas configurações.

O Xano também não tem `CHECK constraint` nem `ON DELETE CASCADE`. Por isso:

- os valores aceitos em `cargo` e nos dois `status` são validados na aplicação,
  a partir das constantes em `petbits/models.py`;
- ao excluir um pedido, a aplicação apaga os itens dele antes (veja
  `PedidoState.delete`).

## 2. Gerar os endpoints CRUD

Para cada tabela, use no Xano a opção de gerar o CRUD automático. Isso cria
cinco endpoints por tabela:

```
GET    /{tabela}          lista todos os registros
GET    /{tabela}/{id}     busca um registro
POST   /{tabela}          cria um registro
PATCH  /{tabela}/{id}     edita um registro
DELETE /{tabela}/{id}     remove um registro
```

Todos precisam ficar no **mesmo API group**, porque a aplicação usa um único
base URL.

> Se o seu workspace gerar o endpoint de edição como `POST /{tabela}/{id}` em
> vez de `PATCH`, mude a constante `METODO_ATUALIZAR` em `petbits/xano.py`. É o
> único lugar do projeto que decide isso.

## 3. Configurar a aplicação

Copie o base URL do API group (no painel do Xano, no topo da tela do API
group). Ele tem este formato:

```
https://x8ki-letl-twmt.n7.xano.io/api:AbCdEf12
```

Na raiz do projeto, copie `.env.example` para `.env` e preencha:

```
XANO_BASE_URL=https://x8ki-letl-twmt.n7.xano.io/api:AbCdEf12
XANO_TOKEN=
```

Deixe `XANO_TOKEN` vazio se o API group estiver público. Se ele exigir
autenticação, cole o token — ele vai no header `Authorization: Bearer ...`.

O arquivo `.env` **não é versionado** (está no `.gitignore`). Cada integrante
do grupo cria o seu.

## 4. Conferir

Com o `.env` preenchido, suba a aplicação:

```bash
reflex run
```

Abra <http://localhost:3000> e cadastre um cliente. Se aparecer uma faixa
vermelha no topo da página, ela traz a mensagem devolvida pelo Xano — as causas
mais comuns são:

| Mensagem | Causa provável |
|---|---|
| `XANO_BASE_URL não configurada` | o `.env` não existe ou está vazio |
| `O Xano respondeu 404` | nome da tabela diferente, ou CRUD não gerado |
| `não autorizado` | o API group exige token e o `XANO_TOKEN` está vazio ou errado |
| `Não foi possível falar com o Xano` | sem internet, ou base URL com erro de digitação |

## Notas de implementação

- **Datas e horas.** O Xano devolve campos `timestamp` como epoch em
  milissegundos e aceita ISO 8601 na escrita. Toda essa tradução fica em
  `petbits/states/conversores.py`.
- **Ordenação.** O CRUD gerado pelo Xano não ordena os resultados; a ordenação
  das listagens é feita em Python, nos States.
- **Filtros.** `TabelaXano.listar_por` filtra em memória, depois de listar. Se
  o volume de dados crescer, crie um endpoint com filtro no Xano e troque só
  esse método.
