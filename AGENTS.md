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

## Ambiente

O projeto usa `venv` + `pip` (não usar `uv`). Sempre ative `.venv` antes de
rodar comandos e registre novas dependências em `requirements.txt` com
`pip freeze > requirements.txt`.

## Convenções deste projeto

- `petbits/models.py` — tabelas SQLModel espelhando o schema `Petshop_DQL`.
- `petbits/database.py` — engine e sessão; a URL vem da variável `DB_URL`.
- `petbits/states/` — um State por entidade, com a lógica de CRUD.
- `petbits/pages/` — uma página por rota, apenas montagem de componentes.
- `petbits/components/` — componentes reutilizáveis (layout, sidebar, UI).
- Setters de estado são declarados explicitamente (`def set_x`), porque os
  setters automáticos do Reflex estão desativados desde a versão 0.9.
- Listas exibidas em tabelas que envolvem join são montadas como `list[dict]`
  no State, já com os nomes das entidades relacionadas resolvidos.
