## Context

O cadastro de produto exige conta de equipe (`exige_equipe`). Quem roda o
script é quem desenvolve, com as contas do `contas-de-teste.local.txt`.

## Decisions

### D1 — Os mesmos caminhos da tela

O script usa `xano.entrar`, `xano.usuario_atual`, `xano.listar_produtos` e
`xano.criar_produto` — as funções do cliente HTTP que as telas usam. As
recusas do backend (nome, preço, estoque, categoria) valem do mesmo jeito.

### D2 — Confere o papel antes de cadastrar

Depois de entrar, o script lê o papel com `/auth/me` e para se não for de
equipe — em vez de deixar cada cadastro voltar 403.

### D3 — Idempotente pelo nome

Lista o catálogo uma vez e pula os nomes que já existem (comparação sem
diferenciar maiúsculas). Rodar duas vezes não duplica.

### D4 — Pausa pelo orçamento

2,2 segundos entre cadastros, como os outros scripts do projeto.

## Risks / Trade-offs

- [A primeira conta de equipe do arquivo não ser a desejada] → A saída diz
  qual conta foi usada (só o e-mail).
