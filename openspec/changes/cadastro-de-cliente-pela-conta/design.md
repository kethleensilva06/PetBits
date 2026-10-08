## Context

- A ficha de tutor (`tutor`) liga-se à conta por `id_user`; `tutor_do_token`
  falha alto se a conta tiver zero ou mais de uma ficha.
- `tutor_cadastro.xs` (público) já resolve documento: normalização, 11
  dígitos, unicidade com recusa genérica e motivo no `event_log`.
- `GET me/tutor` já existe e devolve a ficha da conta, ou nulo.

## Goals / Non-Goals

**Goals:** a conta cria a **própria** ficha, uma vez, com as regras de
documento que já valem.

**Non-Goals:** a equipe criar ficha para outra pessoa; editar ficha.

## Decisions

### D1 — `POST me/tutor`: o dono é o token

Sem `id_user` na entrada. O endpoint lê nome e e-mail da conta com `db.get
user` pelo `$auth.id` e grava `id_user: $auth.id`. É o padrão do
`pet_create.xs`: nada que o cliente mande vira o dono.

### D2 — Uma ficha por conta, sob trava

A conferência "esta conta já tem ficha?" e o `db.add` ficam num
`db.transaction`, com a linha da conta lida com `lock = true`. Duas
requisições simultâneas da mesma conta são serializadas: a segunda vê a ficha
da primeira e é recusada. Sem isso, duas fichas fariam `tutor_do_token` falhar
para sempre naquela conta.

### D3 — Documento: as mesmas regras e a mesma recusa do cadastro público

Mesma normalização (`replace` de `.`, `-`, `/` e espaço), mesmos 11 dígitos,
mesma unicidade por `db.has tutor` — e **a mesma mensagem genérica** quando o
CPF já existe, com o motivo no `event_log`. O endpoint exige login, mas uma
conta qualquer sondando CPFs ainda descobriria quem é cliente da clínica se a
recusa dissesse "CPF em uso".

### D4 — Só conta que não é de tutor pergunta pela ficha

Conta de tutor nasce com ficha (cadastro público), então `PetState.carregar`
só chama `GET me/tutor` quando o papel **não** é de tutor: equipe, ou conta
sem papel. Para tutor o custo da tela não muda; para as outras é uma
requisição a mais.

*Corrigido na aplicação:* a primeira versão perguntava só para equipe. Uma
conta de funcionário criada à mão sem `role` — o erro de operação que a change
`operacao-da-clinica` já previa — caía na lista vazia, sem o formulário.

## Risks / Trade-offs

- [Funcionário digita o CPF de outra pessoa] → Igual ao cadastro público: o
  sistema não valida titularidade de CPF. A ficha fica ligada à conta de quem
  digitou e a clínica corrige no atendimento.
