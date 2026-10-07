## Context

- O padrão de posse do tutor está estabelecido (change `animais-do-tutor`):
  leitura filtrada por `join` até `tutor` e `where` no `$auth.id`; escrita com
  o dono vindo de `PetBits/tutor_do_token`, nunca do corpo.
- O padrão da equipe também (change `operacao-da-clinica`): `auth = "user"`,
  `precondition ($auth.id > 0)` e `PetBits/exige_equipe` como prova, conferido
  pela guarda `scripts/verificar_equipe.py` em todo `equipe_*.xs`.
- O Xano guarda `timestamp` em milissegundos UTC. A clínica funciona no
  horário de São Paulo.
- Orçamento de 10 requisições a cada 20 segundos na instância inteira.

## Goals / Non-Goals

**Goals:** a regra de não-sobreposição e a de expediente valerem **no
backend**, para qualquer requisição; a tela mostrar só horários que o backend
aceitaria.

**Non-Goals:** disponibilidade individual de profissional, remarcação,
escrita da equipe na agenda.

## Decisions

### D1 — `fim` é gravado, não calculado na consulta

`agendamento` guarda `inicio` **e** `fim` (início + duração do serviço no
momento da marcação). Com os dois na linha, "cruza o intervalo" é uma
condição de banco — `inicio < fim_pedido && fim > inicio_pedido` — e não um
`join` até `servico` em cada conferência. Também congela o intervalo: se a
equipe mudar a duração de um serviço depois, os agendamentos já marcados não
passam a se sobrepor retroativamente.

*Alternativa descartada:* calcular `fim` com `join` em `servico` a cada
consulta. Mais uma tabela em toda conferência, e o intervalo de um
agendamento antigo mudaria com o catálogo.

### D2 — Quem decide é o Xano; a tela só sugere

`GET agenda/ocupacao` devolve, para o serviço e o dia, os ids dos
profissionais compatíveis e os intervalos ocupados deles. O Python calcula os
horários livres para mostrar. `POST agendamentos` **refaz** a conta inteira no
Xano — expediente, grade de 30 minutos, futuro, posse do animal, categoria,
profissional livre — e só então grava. A tela errar nunca grava um
agendamento inválido.

*Por que não calcular os horários no Xano:* a grade é um laço de até 20
posições cruzado com os intervalos, e o XanoScript não tem como ser exercitado
aqui antes de publicar. No Python ela é testável localmente; a regra que
**protege** continua no backend.

O tutor recebe ids de profissional e intervalos ocupados — não nome, não
contato. O domínio permite ao tutor saber nome e função de quem atende o
animal dele; ids sem nome não revelam nem isso.

### D3 — Expediente conferido no fuso de São Paulo, pelo próprio Xano

No `POST`, o Xano formata `inicio` e `fim` com
`format_timestamp:"N":"America/Sao_Paulo"` (dia da semana, 1–7) e
`"H:i"` (hora local), e recusa se: o dia for 7 (domingo); o início for antes
de 08:00; o fim passar de 18:00 (seg–sex) ou 12:00 (sábado); o fim cair em
outro dia. A grade de 30 minutos é `inicio % 1800000 == 0`, que vale no fuso
de São Paulo porque o deslocamento é de horas inteiras.

No Python, o mesmo expediente usa um fuso fixo UTC−3. O Brasil não tem
horário de verão desde 2019; se voltar a ter, o Python passa a sugerir
horários que o Xano recusa — falha visível, e não agendamento errado.

### D4 — Profissional escolhido por laço, e conferido de novo depois de gravar

O `POST` lista os profissionais ativos da função compatível (ordem de id) e,
para cada um, conta os agendamentos não cancelados que cruzam o intervalo. O
primeiro com zero é o escolhido. Nenhum livre → recusa.

O Xano não oferece trava entre duas requisições simultâneas. Duas marcações
no mesmo instante podem escolher o mesmo profissional. Por isso, **depois** do
`db.add`, o endpoint conta de novo os agendamentos não cancelados daquele
profissional que cruzam o intervalo; se houver mais de um, marca o recém-criado
como cancelado e recusa com "horário não está mais disponível". Das duas
requisições, pelo menos uma vê a outra — o pior caso é as duas recusarem, e
nunca as duas gravarem.

### D5 — Categoria opcional na tabela, obrigatória para o tutor

`servico.categoria` é `enum?` com `clinica` e `banho_tosa`. Opcional porque já
existem serviços cadastrados e não há como saber qual é qual sem perguntar à
clínica; o `GET servicos` do tutor só devolve os que têm categoria, e o `POST
agendamentos` recusa serviço sem ela. A função compatível é decidida no
backend: `clinica` → `veterinario` ou `clinico_geral`; `banho_tosa` →
`tosador`.

### D6 — Cancelamento: posse pelo join, prazo pelo relógio do Xano

`POST agendamentos/{id}/cancelar` busca o agendamento com `join` até `pet` e
`tutor` e `where` no `$auth.id` — agendamento alheio é indistinguível de
inexistente (404), o mesmo padrão de `pet_get`. Recusa se a situação não for
`marcado` ou se `inicio - now < 24 h`. Grava `situacao = cancelado` e
`cancelado_em = now`; nada é apagado.

### D7 — Situação como enum

`marcado`, `em_andamento`, `concluido`, `cancelado`, como o modelo de domínio
lista. Esta change só usa `marcado` e `cancelado`; os outros dois existem para
a change de histórico clínico não precisar alterar a tabela.

### D8 — Agenda da equipe por dia

`GET equipe/agenda?data=<ms do início do dia>` devolve os agendamentos com
`inicio` dentro de [data, data + 24 h), com `join` até `pet`, `tutor`,
`servico` e `colaborador` e `output` explícito (nome do tutor e telefone, que
a equipe já vê em `equipe/tutores`). Segue o padrão `equipe_*` e entra na
guarda.

## Risks / Trade-offs

- [Requisições simultâneas] → D4: conferência depois de gravar; o pior caso é
  recusa dupla.
- [Horário de verão volta] → D3: o Python sugere errado, o Xano recusa.
- [`GET agenda/ocupacao` mostra a qualquer tutor quanto a clínica está
  ocupada] → É inerente a oferecer horários livres; não revela de quem são os
  agendamentos, nem nomes.
- [Publicação parcial no Xano] → A ordem das tarefas publica tabela e coluna
  antes dos endpoints, cada passo com `--dry-run` antes; endpoints da equipe
  de serviço são republicados só depois de a coluna existir.

## Migration Plan

1. Tabela `agendamento` e coluna `servico.categoria` (aditivas; nada existente
   muda de forma).
2. Endpoints novos; depois os dois de serviço da equipe com a categoria.
3. Telas.
4. A equipe define a categoria dos serviços já existentes pela tela de
   serviços — até lá, o tutor não vê esses serviços.

Desfazer: despublicar os endpoints novos; a tabela e a coluna podem ficar sem
efeito.
