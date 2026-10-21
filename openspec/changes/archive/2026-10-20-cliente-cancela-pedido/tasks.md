## 1. Backend

- [x] 1.1 `pedido_cancelar.xs`: posse pelo join com trava, só `pendente` sem pagamento, estoque devolvido
- [x] 1.2 Validar (`validar_xanoscript.mjs`, `verificar_equipe.py`) e publicar
- [x] 1.3 Provar no Xano: pedido alheio (404), pago (recusa), e o próprio, com o estoque conferido antes e depois

## 2. Tela

- [x] 2.1 `xano.cancelar_pedido`, `LojaState.cancelar_pedido`, `pode_cancelar` em cada pedido
- [x] 2.2 Botão Cancelar pedido com confirmação em Meus pedidos

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador, como Ana: o botão só nos pedidos aguardando pagamento

Medido no Xano: pedido de outra pessoa (19) e inexistente responderam "não
encontrado" e o 19 não mudou; o pago (14) e os prontos (12, 13) foram
recusados; um pedido de teste da Ana (20) levou a areia de 28 a 27, e o
cancelamento a devolveu a 28. Pela tela, o botão só apareceu no pedido de
teste 21, aguardando pagamento, e o cancelou. Os pedidos 20 e 21 ficam no
histórico da conta de teste como cancelados.
