## 1. Xano

- [ ] 1.1 `pedido.origem` (`enum?`, padrão `site`) (D4); publicar a tabela com `--dry-run`
- [ ] 1.2 Função `PetBits/registrar_pedido` (D1, D2)
- [ ] 1.3 `pedido_create.xs` chama a função, com `origem = site`; o comportamento do site não muda
- [ ] 1.4 `equipe_venda_create.xs` (`POST equipe/vendas`): abertura de equipe, cliente conferido no banco (D3), chama a função
- [ ] 1.5 Listas de pedidos (cliente e equipe) devolvem `origem`
- [ ] 1.6 Validar; guarda; publicar nomeados com `--dry-run`; refazer a verificação de entrada sem token do `POST pedidos` (401 com itens válidos, 400 com item sem `produto_id`)

## 2. Reflex

- [ ] 2.1 `/equipe/balcao`: escolher cliente, adicionar produtos à venda, confirmar; item no menu da equipe
- [ ] 2.2 Origem visível em "Meus pedidos" e nos pedidos da equipe

## 3. Verificação

- [ ] 3.1 Com sessão de equipe: vender no balcão para um cliente e ver o pedido entregue e pago na conta dele, com o estoque baixado
- [ ] 3.2 Compra pelo site continua funcionando, com origem `site`
- [ ] 3.3 `openspec validate --strict` (lendo o Totals) e `verificar_equipe.py`
