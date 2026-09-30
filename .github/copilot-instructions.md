# Instruções para o Copilot — PetBits

As regras deste projeto estão em [`AGENTS.md`](../AGENTS.md). Leia-o antes de
qualquer alteração significativa, junto com `docs/project-overview.md` e
`docs/domain-model.md`.

O resumo do que mais importa:

- Mudanças passam pelo OpenSpec (`Explore → Propose → Review → Apply →
  Archive`). Não implementar funcionalidade sem uma change correspondente em
  `openspec/changes/`.
- Cada change é uma **fatia vertical** — uma funcionalidade utilizável de
  ponta a ponta, não uma camada técnica.
- Frontend exclusivamente em Reflex. Ambiente `venv` + `pip`, nunca `uv`.
- Regras de autorização são aplicadas no backend, sempre.
- Escrever em português brasileiro.

> **Atenção:** o comando *Xano: Setup Agent Instructions* da extensão
> `xano.xanoscript` sobrescreve este arquivo e o `AGENTS.md` com um documento
> de orientação sobre XanoScript que **contradiz** o fluxo do projeto (ele
> manda delegar para agentes especializados do Xano em vez de usar o
> OpenSpec). Ele roda sozinho ao entrar com uma conta do Xano. Se isso
> acontecer, restaure com:
>
> ```bash
> git checkout -- AGENTS.md .github/copilot-instructions.md
> ```
