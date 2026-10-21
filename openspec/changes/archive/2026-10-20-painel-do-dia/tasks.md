## 1. Backend

- [x] 1.1 `equipe_painel.xs`: entrada `dia`, agenda do dia sem cancelados e sem contato, três contagens de pedido; comentário reescrito
- [x] 1.2 Validar com `scripts/validar_xanoscript.mjs` e `scripts/verificar_equipe.py`
- [x] 1.3 Publicar com `scripts/publicar.py` e conferir a resposta como equipe e a recusa como tutor

## 2. Tela

- [x] 2.1 `petbits/painel.py`: `agenda_do_dia` e `pedidos_esperando`, com testes em `tests/test_painel.py`
- [x] 2.2 `xano.painel_equipe` recebe o dia; `EquipeState.carregar_painel` preenche a agenda e os pedidos
- [x] 2.3 `EquipeState.abrir_pedidos(situacao)` escolhe o filtro e vai para `/equipe/pedidos`
- [x] 2.4 `painel_page`: Hoje, Pedidos esperando a equipe, os contadores, e o botão Atualizar

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador, como equipe: agenda de hoje, um clique num número de pedido abre a lista filtrada, uma requisição só ao abrir
- [x] 3.3 Roteiro em `docs/project-overview.md`
