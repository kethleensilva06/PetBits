# PetBits

Sistema de gestão para uma clínica veterinária que também opera como petshop.
Frontend em [Reflex](https://reflex.dev), persistência no
[Xano](https://xano.com).

O projeto é desenvolvido com apoio de agentes de IA, seguindo o fluxo do
[OpenSpec](https://github.com/fission-ai/openspec): nenhuma funcionalidade
entra sem uma change correspondente.

## Documentação

| Documento | Responde |
|---|---|
| [`docs/project-overview.md`](docs/project-overview.md) | O que é o projeto |
| [`docs/domain-model.md`](docs/domain-model.md) | Quais são os conceitos e como se relacionam |
| [`AGENTS.md`](AGENTS.md) | Como o agente deve trabalhar no projeto |
| [`openspec/config.yaml`](openspec/config.yaml) | Contexto e regras válidos em toda change |
| `openspec/specs/` | Comportamento consolidado do sistema |
| `openspec/changes/` | O que está sendo planejado ou implementado |

## Ambiente

Python 3.10+, `venv` + `pip` (não usar `uv`).

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

Copie `.env.example` para `.env` e preencha os dois base URLs do Xano.

Execute:

```bash
reflex run
```

A aplicação fica em http://localhost:3000.

> **Windows:** se o `reflex run` abortar com `UnicodeEncodeError: 'charmap'`,
> o console está em cp1252. Rode com `$env:PYTHONUTF8=1; reflex run`.

## Primeiro acesso

A primeira tela é a de entrada, porque o sistema não tem página aberta.

1. Clique em **Cadastre-se** e preencha nome, e-mail, documento e senha.
   A senha precisa de pelo menos 8 caracteres, com uma letra e um número.
2. Ao concluir, você já entra autenticado e cai na tela inicial.
3. Para voltar depois, use **Entrar** com o mesmo e-mail e senha.

A conta criada pelo site é sempre de **tutor** — é isso que permite o
cadastro ser público. O acesso da equipe da clínica chega numa change
própria.

A sessão sobrevive a recarregar a página, a abrir outra aba e a reiniciar o
`reflex run`. Sair limpa tudo.

## Ciclo de desenvolvimento

```text
Explore → Propose → Review → Apply → Archive → próxima change
```

Toda modificação do projeto passa por uma change e termina registrada em
`openspec/changes/archive/`. O que já foi entregue está consolidado em
`openspec/specs/`.
