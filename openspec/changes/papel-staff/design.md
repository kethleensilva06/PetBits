## Context

A regra da change `operacao-da-clinica` (D4) vale integralmente: papel se
confere por **igualdade com o valor esperado**, nunca por negação do outro
valor nem por teste de nulidade — `!= "member"` deixaria passar conta sem
papel. Até aqui o valor esperado era um só, `admin`.

## Decisions

### D1 — Dois valores, cada um por igualdade

No Xano: `precondition (($conta.role == "admin") || ($conta.role == "staff"))`.
`==` e `||` já rodam no motor nesta conta (é a forma provada que os
`equipe_servico_*` usam). Conta sem papel, ou com qualquer outro valor, falha
as duas igualdades e é recusada com a mesma mensagem de antes.

No Python, `PAPEIS_EQUIPE = ("admin", "staff")` substitui `PAPEL_EQUIPE`, e
`eh_equipe` passa a ser `papel in PAPEIS_EQUIPE`. Continua sendo o único lugar
do Python que compara com as strings cruas.

### D2 — O enum do repositório acompanha o Xano, sem republicar a tabela

`staff` foi criado no painel, fora do repositório. O arquivo
`tables/898256_user.xs` passa a registrar `["admin", "staff", "member"]`, que
é o que o `workspace pull` mostrou. A tabela não é publicada nesta change: ela
é `xano:quick-start` e é a tabela da qual o login inteiro depende; republicá-la
sem necessidade é risco sem ganho.

## Risks / Trade-offs

- [`staff` e `admin` com o mesmo acesso] → É o que a clínica pediu agora;
  diferenciar fica fora do escopo e vira change própria.
- [Outro valor novo criado no painel no futuro] → Cai como "papel
  desconhecido", sem acesso, como deve: a recusa é o comportamento seguro.
