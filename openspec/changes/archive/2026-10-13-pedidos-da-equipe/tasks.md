## 1. Xano

- [x] 1.1 `equipe_pedido_list.xs` (`GET equipe/pedidos`): D1, abertura de equipe
- [x] 1.2 `equipe_pedido_situacao.xs` (`POST equipe/pedidos/{pedido_id}/situacao`): D2, D3, D4
- [x] 1.3 Validar com o parser; guarda `verificar_equipe.py`; publicar os dois nomeados, com `--dry-run`; sem token recusam

## 2. Reflex

- [x] 2.1 Regra das transições também em Python, para a tela só oferecer os botões válidos; testada com todas as combinações de situação e entrega
- [x] 2.2 `/equipe/pedidos` com filtro por situação, itens, e botões de ação; item no menu da equipe — **Verificada em 13/10, no navegador:** filtro por situação, pedidos com situação, itens, totais e forma de entrega, e os três botões de ação (Marcar como pago, Pronto para retirada, Cancelar); item **Pedidos** no menu.
      Os botões só apareceram depois de existir um pedido **pendente** — todos os da base estavam em estado terminal, e tela sem o que acionar não prova que o controle existe. Criei o pedido nº 12 pelo lado do cliente para a verificação ser real

## 3. Verificação

- [x] 3.1 Com sessão de equipe: marcar pronto, entregar com pagamento na retirada, cancelar e ver o estoque voltar — verificado pela ponta a ponta de 2026-10-11 (25/25 no Xano de verdade)
- [x] 3.2 Caminho inválido por requisição direta é recusado — verificado pela ponta a ponta de 2026-10-11 (25/25 no Xano de verdade)
- [x] 3.3 `openspec validate --strict` (lendo o Totals) e `verificar_equipe.py` — **Situação:** em 2026-10-11, depois da change `limpar-endpoints-fora-do-ar`: `validate --all --strict` sem falha e `verificar_equipe.py` sem acusação
