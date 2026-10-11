## 1. Xano

- [x] 1.1 `pedido.origem` (`enum?`, padrão `site`) (D4); publicar a tabela com `--dry-run`
- [x] 1.2 Função `PetBits/registrar_pedido` (D1, D2)
- [x] 1.3 `pedido_create.xs` chama a função, com `origem = site`; o comportamento do site não muda
- [x] 1.4 `equipe_venda_create.xs` (`POST equipe/vendas`): abertura de equipe, cliente conferido no banco (D3), chama a função
- [x] 1.5 Listas de pedidos (cliente e equipe) devolvem `origem`
- [x] 1.6 Validar; guarda; publicar nomeados com `--dry-run`; refazer a verificação de entrada sem token do `POST pedidos` (401 com itens válidos, 400 com item sem `produto_id`)

## 2. Reflex

- [ ] 2.1 `/equipe/balcao`: escolher cliente, adicionar produtos à venda, confirmar; item no menu da equipe — **Situação:** construída e compila; a venda passou na ponta a ponta; falta ver a tela no navegador
- [x] 2.2 Origem visível em "Meus pedidos" e nos pedidos da equipe

## 3. Verificação

- [x] 3.1 Com sessão de equipe: vender no balcão para um cliente e ver o pedido entregue e pago na conta dele, com o estoque baixado — verificado pela ponta a ponta de 2026-10-11 (25/25 no Xano de verdade)
- [ ] 3.2 Compra pelo site continua funcionando, com origem `site` — **Situação:** a compra pelo site passou na ponta a ponta; a origem `site` não foi conferida por ela
- [ ] 3.3 `openspec validate --strict` (lendo o Totals) e `verificar_equipe.py`
