## Why

A tela Agendar tem os passos numerados, mas espalhados em duas colunas: o
serviço e o animal à esquerda, o calendário, as observações e o confirmar à
direita. O tutor não vê em que passo está nem o que falta, e o que vai ser
marcado só aparece numa frase depois de escolher o horário. Depois de marcar,
o compromisso fica só no site.

## What Changes

- Uma faixa de progresso no alto: **1 Serviço → 2 Animal → 3 Horário →
  4 Confirmar**, com os feitos marcados e o atual destacado.
- Os passos ficam numa coluna só, na ordem da faixa.
- Ao lado, um **resumo fixo** com serviço, duração, preço, animal, dia e
  horário, cada linha dizendo "a escolher" até ser escolhida, e o botão
  Confirmar. No celular, o resumo vem depois dos passos.
- Depois de marcar, o aviso de sucesso traz **"Adicionar à agenda do
  celular"**, que baixa um arquivo `.ics` com o compromisso. O arquivo é
  montado na própria tela, sem requisição ao Xano.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `agendamentos`: a tela de agendar guia o tutor e oferece o compromisso para a agenda do celular.

## Fora do escopo

- Mudar as regras de horário livre ou de cancelamento.
- Lembrete por e-mail ou mensagem.

## Impact

- Código: `petbits/calendario.py` (novo), `petbits/states/agenda_state.py`,
  `petbits/pages/agenda.py`; `tests/test_calendario.py`, `tests/test_agenda_guiada.py`.
- Backend: nenhum.
