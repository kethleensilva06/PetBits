## 1. Medição

- [x] 1.1 Medir `object[]` na entrada pelo próprio `POST pedidos`, sem token: o Xano valida a entrada antes do login, então itens válidos devem dar 401 e item sem `produto_id` deve dar 400. Sem endpoint descartável — o CLI não remove um endpoint isolado, só por `push --sync --delete`, que apagaria tudo que não estivesse na pasta. O `foreach` sobre a lista é exercitado na 6.2 (D2)

## 2. Tabelas

- [x] 2.1 `produto`, `pedido`, `pedido_item` (D1); validar; publicar com `--dry-run` antes; conferir por `pull`

## 3. Endpoints da equipe

- [ ] 3.1 `equipe_produto_list.xs`, `equipe_produto_create.xs`, `equipe_produto_update.xs` com a abertura de equipe; recusas de nome vazio, preço ≤ 0 e estoque negativo, na criação e na alteração; `pick` na alteração; verificar que a guarda passa com eles — **Situação:** publicados em 2026-10-09; a guarda passa com 15 endpoints; sem token recusam. Falta exercitar as recusas com sessão de equipe (6.1)

## 4. Endpoints do cliente

- [ ] 4.1 `loja_produtos.xs` (`GET loja/produtos`): ativos com estoque > 0, `output` explícito — **Situação:** publicado em 2026-10-09; sem token recusa. Falta ver a lista com sessão de cliente (6.2)
- [ ] 4.2 `pedido_create.xs` (`POST pedidos`): D2, D3, D4; dono pelo token — **Situação:** publicado em 2026-10-09; a entrada `object[]` foi medida (1.1). Falta exercitar compra, estoque e recusas com sessão de cliente (6.2, 6.3)
- [ ] 4.3 `pedido_list.xs` (`GET pedidos`): D5, só do cliente do token — **Situação:** publicado em 2026-10-09; sem token recusa. Falta ver com sessão de cliente (6.2)
- [x] 4.4 Publicar os endpoints nomeados um a um, com `--dry-run`; sem token, todos recusam

## 5. Reflex

- [ ] 5.1 Cliente HTTP em `petbits/xano.py`
- [ ] 5.2 `/equipe/produtos`: lista, criar, editar, ativar/desativar; item no menu da equipe
- [ ] 5.3 `/loja`: grade de produtos, carrinho, finalização com entrega e pagamento (aviso de pagamento simulado); bloqueio de funcionário (D6)
- [ ] 5.4 `/pedidos`: meus pedidos com itens; links na casa do cliente
- [ ] 5.5 O `sair` limpa os estados novos

## 6. Verificação

- [ ] 6.1 Equipe no navegador: cadastrar um produto, alterar só o preço, desativar e reativar
- [ ] 6.2 Cliente no navegador (feito por quem tem a senha, ou com a sessão aberta): comprar com retirada e pagamento na loja, e com entrega e pagamento online; ver em "Meus pedidos"; conferir que o estoque baixou
- [ ] 6.3 Recusas: estoque insuficiente sem mudar estoque nenhum; produto inativo; pedido vazio
- [ ] 6.4 `openspec validate --strict` (lendo o Totals) e `verificar_equipe.py`
