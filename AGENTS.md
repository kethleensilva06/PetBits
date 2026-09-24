<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** � up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above � do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs � components, state management, events, styling, database, routing, authentication � use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available � always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->

## Frontend

O frontend do projeto deve ser implementado exclusivamente com Reflex.

Utilize os mecanismos próprios do Reflex para componentes, estado, eventos,
páginas e interação. Não introduza outra tecnologia de frontend para substituir
ou complementar o Reflex, salvo quando houver uma alteração arquitetural
explicitamente aprovada.

## Banco de dados

O banco de dados fica hospedado no **Xano** e é acessado por HTTP. O projeto
não tem banco local nem ORM: não reintroduza SQLModel, SQLAlchemy, Alembic nem
o ORM interno do Reflex (`rx.Model`, `rx.session`).

Toda comunicação com o Xano passa por `petbits/xano.py`. Nenhum outro módulo
deve falar HTTP nem montar URLs.

As credenciais vêm do arquivo `.env` (modelo em `.env.example`), que **não é
versionado**. A estrutura das tabelas e o passo a passo de configuração estão
em `docs/xano-setup.md`.

## Ambiente

O projeto usa `venv` + `pip` (não usar `uv`). Sempre ative `.venv` antes de
rodar comandos e registre novas dependências em `requirements.txt` com
`pip freeze > requirements.txt`.

## Convenções deste projeto

- `petbits/xano.py` — cliente HTTP do Xano (`TabelaXano`, `XanoError`); o base
  URL vem de `XANO_BASE_URL`.
- `petbits/models.py` — descreve as tabelas do Xano e expõe um acessor por
  tabela (`models.clientes`, `models.pets`, ...), além das constantes de
  domínio fechado (cargos e status).
- `petbits/states/` — um State por entidade, com a lógica de CRUD.
- `petbits/states/conversores.py` — tradução entre os valores dos formulários
  HTML e o JSON do Xano (datas, horas e moeda).
- `petbits/pages/` — uma página por rota, apenas montagem de componentes.
- `petbits/components/` — componentes reutilizáveis (layout, sidebar, UI).
- Setters de estado são declarados explicitamente (`def set_x`), porque os
  setters automáticos do Reflex estão desativados desde a versão 0.9.
- Registros do Xano circulam como `dict` (nunca como objeto de modelo). As
  listas exibidas em tabelas são montadas no State como `list[dict]`, já com
  os nomes das entidades relacionadas resolvidos e os valores formatados.
- Event handlers que falam com o Xano são `async` e usam `await`. Os `@rx.var`
  permanecem sincronos: eles apenas filtram listas já carregadas.
- Falhas de rede não devem quebrar a tela. Cada State expõe `load_error`, e
  cada página mostra esse texto com `error_banner(...)`.
- O plano gratuito do Xano aceita **10 requisições a cada 20 segundos**.
  `petbits/xano.py` controla isso sozinho (janela deslizante + retry no 429),
  mas evite acrescentar chamadas desnecessárias: o painel já consulta sete
  tabelas. Prefira reaproveitar dados já carregados no State a refazer a busca.
- O Xano não impõe `CHECK`, `UNIQUE` nem `ON DELETE CASCADE`: essas regras são
  responsabilidade dos States (validação antes de gravar e remoção explícita
  dos registros dependentes).
