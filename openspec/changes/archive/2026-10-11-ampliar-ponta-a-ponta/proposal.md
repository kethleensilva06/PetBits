## Why

A primeira rodada da verificação de ponta a ponta (25/25) fechou boa parte
das tarefas abertas, mas várias recusas das specs continuam sem ter rodado
com sessão de verdade: expediente e horário no passado na agenda, animal de
outro cliente, duas contas, entrega no endereço, estoque negativo, produto
inativo, pedido vazio, categoria inválida, e a regra da gerência
(equipe comum não mantém colaboradores). Cada uma, hoje, depende de alguém
fazer o caminho à mão.

O próprio script também só foi testado com um Xano simulado descartável;
nada impede que ele quebre em silêncio.

## What Changes

- `scripts/verificar_ponta_a_ponta.py` ganha os cenários de recusa que
  faltam, usando também a **segunda** conta de cliente do arquivo para as
  conferências de duas contas.
- Um cenário que deixaria dado impossível de desfazer é **pulado com o motivo
  escrito**: o cancelamento com menos de 24 h exigiria marcar um agendamento
  que depois ninguém consegue cancelar pelo sistema.
- `tests/test_ponta_a_ponta.py`: o script roda contra um Xano simulado em
  memória que aplica as regras das specs — com o backend certo, todos passam;
  com uma regra quebrada de propósito, o script acusa.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `verificacao`: a ponta a ponta cobre as recusas e as conferências de duas
  contas, e tem teste próprio.

## Fora do escopo

- Conferir as telas: continua sendo no navegador.

## Impact

- `scripts/verificar_ponta_a_ponta.py`, `tests/test_ponta_a_ponta.py`.
- A rodada passa a usar duas contas de cliente e deixa um pouco mais de dado
  de teste reconhecível no Xano (pedidos cancelados, produtos de verificação
  desativados).
