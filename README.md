# PetBits

Frontend em [Reflex](https://reflex.dev) para o sistema de gestão de uma clínica
veterinária / petshop, com o banco de dados hospedado no
[Xano](https://xano.com).

## Rodando o projeto

```bash
python -m venv .venv
```

Ative o ambiente (Windows PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o acesso ao Xano copiando `.env.example` para `.env` e preenchendo
os dois base URLs (são dois API groups: o do domínio e o de autenticação):

```
XANO_BASE_URL=https://seu-workspace.xano.io/api:xxxxxxxx
XANO_AUTH_BASE_URL=https://seu-workspace.xano.io/api:yyyyyyyy
```

Execute:

```bash
reflex run
```

A aplicação fica disponível em http://localhost:3000.

### Primeiro acesso

A primeira tela é o login, e no começo não existe conta nenhuma:

1. **Cadastre-se** — a conta nasce como tutor e já cai no portal, onde dá para
   cadastrar um pet e marcar consulta.
2. Para administrar a clínica, promova essa conta:

   ```bash
   python scripts/promover_admin.py voce@email.com
   ```

3. Saia e entre de novo: agora você cai no painel.

> **Windows:** se o `reflex run` abortar com `UnicodeEncodeError: 'charmap'
> codec can't encode character`, o console está em cp1252 e não consegue
> escrever os caracteres da barra de progresso. Rode com UTF-8:
>
> ```bash
> $env:PYTHONUTF8=1; reflex run
> ```

## Banco de dados

O banco fica no Xano e é acessado por HTTP — a aplicação não tem banco local
nem ORM. As nove tabelas, seus campos e o passo a passo de configuração estão
em [`docs/xano-setup.md`](docs/xano-setup.md).

Se a aplicação não conseguir falar com o Xano, cada página mostra uma faixa
vermelha com a mensagem devolvida pela API, em vez de quebrar.

## Dois perfis

| | Tutor | Equipe da clínica |
|---|---|---|
| Entra por | cadastro no site | promoção de uma conta existente |
| Cai em | `/portal` | `/` |
| Vê | os próprios pets, consultas, histórico e compras | as nove telas de gestão |

A separação é feita no **backend**: os 45 endpoints do Xano exigem login, e
cada um confere o papel e o dono da linha antes de responder. O que o
navegador guarda serve para esconder botão, nunca para proteger dado — quem
barra está em [`docs/xanoscript.md`](docs/xanoscript.md).

## Estrutura

```
petbits/
├── xano.py            # cliente HTTP do Xano (único módulo que fala HTTP)
├── models.py          # tabelas do Xano e constantes de domínio
├── petbits.py         # app e registro das rotas
├── components/        # layout, sidebar e componentes de UI reutilizáveis
├── pages/             # uma página por rota
└── states/            # um State por entidade, com a lógica de CRUD
    ├── auth_state.py  # sessão: login, cadastro e papel de quem entrou
    ├── sessao.py      # a guarda que todo load_* atravessa
    ├── portal_state.py# as seis telas do tutor, num State só
    └── conversores.py # tradução entre formulários HTML e o JSON do Xano

scripts/
└── promover_admin.py  # transforma uma conta em administradora
```

## Rotas

| Rota | Página | Tabelas |
|------|--------|---------|
| `/` | Painel com indicadores e próximos agendamentos | todas |
| `/clientes` | Cadastro de tutores | `cliente` |
| `/pets` | Cadastro de pets | `pet` → `cliente` |
| `/agendamentos` | Agenda de serviços | `agendamento` → `pet`, `servico`, `funcionario` |
| `/prontuarios` | Histórico clínico | `prontuario` → `pet`, `funcionario` |
| `/servicos` | Catálogo de serviços | `servico` |
| `/produtos` | Catálogo de produtos | `produto` |
| `/pedidos` | Pedidos e seus itens | `pedido`, `itens_pedido` → `produto` |
| `/funcionarios` | Equipe | `funcionario` |

## Arquitetura do frontend

Cada entidade segue o mesmo padrão:

- **State** (`petbits/states/`): guarda a lista exibida, os campos do formulário
  e os métodos `load_*`, `open_new`, `open_edit`, `save` e `delete`. O
  carregamento inicial acontece no `on_load` da rota, declarado em `petbits.py`.
  Os métodos que falam com o Xano são `async`.
- **Página** (`petbits/pages/`): monta a barra de busca, a tabela e o diálogo de
  formulário, ligando os componentes aos eventos do State.
- **Componentes** (`petbits/components/`): `layout` (sidebar + cabeçalho),
  `sidebar` (navegação) e helpers de UI (`form_field`, `row_actions`,
  `empty_state`, `page_toolbar`, `error_banner`).

Os registros vindos do Xano circulam como dicionários. Cada State monta a lista
exibida como `list[dict]`, já com os nomes das entidades relacionadas resolvidos
(pets com o nome do tutor, agendamentos com pet/serviço/responsável) e com datas
e valores formatados — assim a renderização não precisa fazer requisições nem
conversões.

Como o Xano não impõe `CHECK`, `UNIQUE` nem `ON DELETE CASCADE`, essas regras
ficam nos States: os valores de `cargo` e `status` vêm das constantes de
`petbits/models.py`, e a exclusão de um pedido remove antes os seus itens.
