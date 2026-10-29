## Why

A revisão do backend pedida pela usuária achou dois pontos:

- Alguns filtros ainda leem a tabela inteira por falta de índice, em tabelas
  que crescem com o uso: o e-mail do tutor, os atendimentos por profissional e
  os agendamentos por serviço. `user.email` e `tutor.documento` já têm índice
  único. Colaboradores, serviços e produtos ficam como estão: são tabelas de
  dezenas de linhas, e `tables/colaborador.xs` já registra que índice ali não
  compensa.
- A lista de Pedidos da equipe traz **todos** os pedidos da história, com
  **todos** os itens de todos eles, a cada abertura. É a única lista que cresce
  sem parar.

Tutores e animais continuam completos: a busca da tela é feita sobre a lista
inteira, as consultas já devolvem só as colunas usadas e vêm ordenadas por um
campo com índice. Um endpoint único para a casa do cliente também saiu do
plano: com as telas guardadas, a casa só pede ao Xano na primeira abertura.

## What Changes

- Novos índices: `tutor.email`, `atendimento.id_colaborador`,
  `agendamento.id_servico` e `pedido.created_at` (para o período).
- `GET equipe/pedidos` aceita `dias`: só os pedidos (e os itens) dos últimos
  `dias` dias; vazio ou 0 traz todo o período.
- A tela de Pedidos da equipe ganha o filtro **Período**: últimos 90 dias (o
  padrão), últimos 30 dias ou todo o período. O resumo e o CSV seguem o que
  está na tela.
- Vir do painel para Pedidos (pedidos esperando) abre com todo o período, para
  nenhum pedido pendente antigo ficar de fora.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: a equipe vê os pedidos por período.
- `desempenho`: os filtros do backend usam índices.

## Impact

- Xano: `tables/tutor.xs`, `tables/atendimento.xs`, `tables/agendamento.xs`,
  `tables/pedido.xs`,
  `apis/pet_bits/equipe_pedido_list.xs`.
- Código: `petbits/xano.py`, `petbits/states/equipe_state.py`,
  `petbits/pages/equipe.py`; testes.
