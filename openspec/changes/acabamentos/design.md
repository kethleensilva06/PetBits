## Context

Levantado na visão geral do projeto: duplicações que já existem em três ou
quatro lugares e defeitos pequenos. A regra que vale: nada aqui muda
comportamento, exceto a saudação.

## Decisions

### D1 — Funções, não herança, para a guarda de sessão

`sessao.token_de_cliente(state, destino_sem_sessao)` e
`sessao.encerrar(state, erro)` são funções assíncronas que recebem o State.
Herança entre States do Reflex cria subestados e muda nomes de eventos; uma
função comum não mexe em nada disso. Cada State continua com seu `_token`,
agora de uma linha, para os carregadores não mudarem.

### D2 — Rótulos num módulo puro

`petbits/rotulos.py` sem Reflex, importável pelos testes. Os nomes antigos
(`CATEGORIAS`, `SITUACOES` em `loja_state`, etc.) continuam como apelidos onde
outros arquivos já os importam, para a mudança não se espalhar.

### D3 — A regra da categoria vira função no Xano

`PetBits/funcoes_da_categoria` recebe a categoria e devolve `{a, b}` — as duas
funções de colaborador que atendem (`veterinario`/`clinico_geral` para
clínica, `tosador` duas vezes para banho e tosa). Os endpoints passam a
chamá-la. Publicação por `scripts/publicar.py`, com prévia.

## Risks / Trade-offs

- [A função do Xano mudar o comportamento da agenda] → Mesma regra, mesmos
  valores; a verificação de ponta a ponta exercita `agenda/ocupacao` e o
  `POST agendamentos` com sessão.
