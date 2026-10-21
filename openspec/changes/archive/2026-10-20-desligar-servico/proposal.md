## Why

Apareceram na lista de serviços da clínica dois "Sonda" (R$ 1,00, sem
categoria), e dois colaboradores "Sonda". A origem é o
`scripts/teste_duas_contas.py`: ele chama cada endpoint de equipe com a conta
de cliente (tem de dar 403) e com a de equipe (tem de passar) — e, para a
equipe, o `POST` é de verdade. Cada rodada deixa um serviço e um colaborador.

Os colaboradores podem ser desligados; os serviços, não: o serviço não tem
"ativo", e um serviço que a clínica deixou de oferecer — ou um criado por
engano — fica na lista para sempre.

## What Changes

- **Desligar e religar serviço:** coluna `ativo` em `servico`, que nasce
  `true`; o `PATCH` da equipe aceita
  `ativo`; a tela de serviços ganha "Desativar"/"Ativar" e o selo "Inativo",
  como a de produtos.
- **Serviço inativo não é oferecido:** sai da lista do tutor, e o
  agendamento e a ocupação recusam como "não está disponível". Agendamentos
  já marcados não mudam.
- **O script deixa de criar dados:** as sondas de escrita mandam nome só de espaços.
  A equipe recebe 400 — passou pela prova, e a validação recusou antes de
  gravar —, o cliente continua recebendo 403, e nada é criado.
- No fim, os dois serviços "Sonda" são desativados (os colaboradores já
  foram, em 19/10).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `servicos`: desligar e religar serviço; serviço inativo não é agendável.
- `verificacao`: o teste das duas contas não grava nada.

## Fora do escopo

- Apagar serviço: como o colaborador, serviço desligado continua sendo o que
  foi prestado nos agendamentos antigos.
- Cancelar agendamentos futuros de um serviço desligado.

## Impact

- Xano: `tables/servico.xs`; `equipe_servico_update.xs`,
  `equipe_servico_list.xs`, `equipe_servico_get.xs`, `servico_list_tutor.xs`,
  `agendamento_create.xs`, `agenda_ocupacao.xs` republicados.
- Reflex: `petbits/pages/equipe.py`, `petbits/states/equipe_state.py`.
- Scripts e testes: `scripts/teste_duas_contas.py`; teste novo.
