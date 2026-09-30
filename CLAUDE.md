# CLAUDE.md — PetBits

As regras deste projeto estão em **[`AGENTS.md`](AGENTS.md)**. Leia-o antes de
qualquer alteração significativa, junto com `docs/project-overview.md` e
`docs/domain-model.md`.

O fluxo é o do OpenSpec: `Explore → Propose → Review → Apply → Archive`.
Nenhuma funcionalidade entra sem uma change em `openspec/changes/`.

> **Atenção:** o comando *Xano: Setup Agent Instructions* da extensão
> `xano.xanoscript` sobrescreve este arquivo e o `AGENTS.md` com um documento
> sobre XanoScript que **contradiz** o fluxo do projeto — ele manda delegar
> para agentes especializados do Xano em vez de usar o OpenSpec. Ele roda
> sozinho ao entrar com uma conta do Xano. Se acontecer, restaure com:
>
> ```bash
> git checkout -- AGENTS.md CLAUDE.md .github/copilot-instructions.md
> ```
