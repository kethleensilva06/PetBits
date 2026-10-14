## 1. Medição

- [x] 1.1 Medir `object[]` na entrada pelo próprio `POST pedidos`, sem token: o Xano valida a entrada antes do login, então itens válidos devem dar 401 e item sem `produto_id` deve dar 400. Sem endpoint descartável — o CLI não remove um endpoint isolado, só por `push --sync --delete`, que apagaria tudo que não estivesse na pasta. O `foreach` sobre a lista é exercitado na 6.2 (D2)

## 2. Tabelas

- [x] 2.1 `produto`, `pedido`, `pedido_item` (D1); validar; publicar com `--dry-run` antes; conferir por `pull`

## 3. Endpoints da equipe

- [x] 3.1 `equipe_produto_list.xs`, `equipe_produto_create.xs`, `equipe_produto_update.xs` com a abertura de equipe; recusas de nome vazio, preço ≤ 0 e estoque negativo, na criação e na alteração; `pick` na alteração; verificar que a guarda passa com eles — **Situação:** publicados; a ponta a ponta provou preço zero recusado; a rodada da ponta a ponta ampliada em 2026-10-11 provou estoque negativo recusado na criação e na alteração, categoria inválida recusada e que alterar só o preço mantém o resto

## 4. Endpoints do cliente

- [x] 4.1 `loja_produtos.xs` (`GET loja/produtos`): ativos com estoque > 0, `output` explícito — verificado pela ponta a ponta de 2026-10-11 (25/25 no Xano de verdade)
- [x] 4.2 `pedido_create.xs` (`POST pedidos`): D2, D3, D4; dono pelo token — verificado pela ponta a ponta de 2026-10-11 (25/25 no Xano de verdade)
- [x] 4.3 `pedido_list.xs` (`GET pedidos`): D5, só do cliente do token — verificado pela ponta a ponta de 2026-10-11 (25/25 no Xano de verdade)
- [x] 4.4 Publicar os endpoints nomeados um a um, com `--dry-run`; sem token, todos recusam

## 5. Reflex

- [x] 5.1 Cliente HTTP em `petbits/xano.py`
- [x] 5.2 `/equipe/produtos`: lista, criar, editar, ativar/desativar; item no menu da equipe — **Vista na tela em 13/10, com sessão de gerência:** lista com categoria, preço, estoque, marca, embalagem e descrição; botões Desativar e Editar em cada cartão; botão Novo produto; item **Produtos** no menu
- [x] 5.3 `/loja`: grade de produtos, carrinho, finalização com entrega e pagamento (aviso de pagamento simulado); bloqueio de funcionário (D6) — **Vista na tela em 13/10:** grade com categoria, marca, nome, embalagem, descrição, preço e disponibilidade; carrinho com item, quantidade e total; finalização com as duas entregas e as duas formas de pagamento. O aviso aparece **só** ao escolher pagar online: "Pagamento SIMULADO: nenhum valor é cobrado e nenhum dado de cartão é pedido". E o D6: conta de equipe comum abrindo `/loja` foi levada para `/equipe`.
      De passagem, os três "Produto de verificação" inativos **não aparecem** na grade — a regra de que produto inativo não chega ao cliente, vista funcionando
- [x] 5.4 `/pedidos`: meus pedidos com itens; links na casa do cliente — **Vista na tela em 13/10:** cada pedido com número, situação, total, data, origem, forma de entrega, forma de pagamento e os itens; o de entrega no endereço mostra o endereço do cadastro. Links no menu do cliente
- [x] 5.5 O `sair` limpa os estados novos

## 6. Verificação

- [x] 6.1 Equipe no navegador: cadastrar um produto, alterar só o preço, desativar e reativar — **Os quatro gestos feitos na tela em 13/10**, cada um confirmado por recarga: cadastrar (diálogo preenchido, produto na lista); alterar só o preço (34,90 → 27,50, com categoria, marca, embalagem e estoque intactos); desativar (selo *Inativo*, botão vira *Ativar*); reativar (selo some, botão volta a *Desativar*).
      Confirmar por recarga não é zelo: numa primeira tentativa o clique "deu certo" e o estado não mudou — o painel estava servindo DOM velho, e só a recarga mostrou isso
- [x] 6.2 Cliente no navegador: comprar com retirada e pagamento na loja, e com entrega e pagamento online; ver em "Meus pedidos"; conferir que o estoque baixou — **Feito na tela em 13/10, as duas compras:** pedido nº 13 (retirada, pagamento na loja) saiu *Aguardando pagamento*; pedido nº 14 (entrega no endereço, pagamento online) saiu *Pago* e com o endereço do cadastro. Os dois aparecem em Meus pedidos com os itens.
      **O estoque baixou na tela:** o produto comprado passou de 12 para 11 disponíveis, visto na própria grade da loja depois da compra
- [x] 6.3 Recusas: estoque insuficiente sem mudar estoque nenhum; produto inativo; pedido vazio — verificado pela ponta a ponta de 2026-10-11 (25/25 no Xano de verdade)
- [x] 6.4 `openspec validate --strict` (lendo o Totals) e `verificar_equipe.py` — **Situação:** em 2026-10-11, depois da change `limpar-endpoints-fora-do-ar`: `validate --all --strict` sem falha e `verificar_equipe.py` sem acusação
