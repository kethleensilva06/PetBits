## 1. Fotos

- [x] 1.1 Escolher as 14 fotos no Unsplash/Pexels (cão, gato, outro animal, banner, seis categorias + genérica, três telas vazias) e anotar página, autor e licença (D1) — escolhidas no Unsplash com o filtro de licença livre, conferidas numa prancha antes do download
- [x] 1.2 Pedir autorização com a lista (nome, origem, tamanho) e baixar para `assets/fotos/` no tamanho de tela (D2); `CREDITOS.md` — autorizado e baixado em 19/10, WebP 600 px (banner 1200 px, 170 KB depois de rebaixado com qualidade menor)
- [x] 1.3 Uma foto por produto do catálogo, escolhida pelo nome e pela descrição (D4) — 15 dos produtos de exemplo e a "Escova removedora de pelos" que a equipe cadastrou; três candidatas trocadas na conferência (saco de ração de outra marca, tapete e comedouro que não apareciam no recorte). Cada lote baixado só depois de autorizado

## 2. Código

- [x] 2.1 `petbits/ilustracoes.py` aponta para `/fotos/` (D3); remover `assets/ilustracoes/`
- [x] 2.2 `rx.image` com `object_fit="cover"` e recorte arredondado na casa, na loja e em `tela_vazia`
- [x] 2.3 `imagem_do_produto` com a chave do nome e a categoria de reserva (D4); `LojaState` usa ela
- [x] 2.4 Detalhe do produto num diálogo (D5): foto grande, dados, "No carrinho: N" e adicionar

## 3. Verificação

- [x] 3.1 `tests/test_ilustracoes.py` com a conferência de créditos; a suíte toda passa — **76 testes, OK**, incluindo: toda foto (30) tem linha em `CREDITOS.md`; todo produto de exemplo tem foto própria; produto novo cai na categoria
- [x] 3.2 Navegador como tutora: casa, loja, telas vazias; claro, escuro e celular; sem requisição externa nova — **Visto em 19/10 como Ana:** casa com o banner (cão e gato) e os avatares por espécie; loja com os 17 produtos, 16 com foto própria e o "Produto de verificação" com a da categoria; clicar na foto da Areia abriu o detalhe com marca, embalagem, descrição e preço, "Adicionar ao carrinho" pôs 1 no carrinho e mostrou "No carrinho: 1", Esc fechou com o carrinho intacto; no celular, o detalhe pelo nome do Arranhador ocupou 343 de 375 px, sem rolagem lateral; casa em escuro e celular sem rolagem lateral. Domínios externos carregados: só `fonts.googleapis.com` e `fonts.gstatic.com` (a fonte).
      As telas vazias usam o mesmo `tela_vazia` já visto na `cliente-ilustrado`; com a Ana (que tem animais, pedidos e agendamentos) elas não aparecem, e a troca foi só do arquivo de imagem
- [x] 3.3 `openspec validate fotos-realistas --strict`
