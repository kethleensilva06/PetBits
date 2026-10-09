## 1. Xano

- [ ] 1.1 `equipe_pedido_list.xs` (`GET equipe/pedidos`): D1, abertura de equipe
- [ ] 1.2 `equipe_pedido_situacao.xs` (`POST equipe/pedidos/{pedido_id}/situacao`): D2, D3, D4
- [ ] 1.3 Validar com o parser; guarda `verificar_equipe.py`; publicar os dois nomeados, com `--dry-run`; sem token recusam

## 2. Reflex

- [ ] 2.1 Regra das transições também em Python, para a tela só oferecer os botões válidos; testada com todas as combinações de situação e entrega
- [ ] 2.2 `/equipe/pedidos` com filtro por situação, itens, e botões de ação; item no menu da equipe

## 3. Verificação

- [ ] 3.1 Com sessão de equipe: marcar pronto, entregar com pagamento na retirada, cancelar e ver o estoque voltar
- [ ] 3.2 Caminho inválido por requisição direta é recusado
- [ ] 3.3 `openspec validate --strict` (lendo o Totals) e `verificar_equipe.py`
