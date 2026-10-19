## 1. Tema

- [x] 1.1 `rx.theme` no `rx.App` (D1) e a Nunito em `stylesheets`
- [x] 1.2 `assets/estilo.css`: fonte nas variáveis do Radix e fundo com degradê do tema (D2)

## 2. Componentes comuns

- [x] 2.1 `petbits/visual.py` com `marca`, `pilula` e `topo_do_cliente` (D3) — mais `barra`, `sair` e `titulo_de_pagina`, usados nas duas áreas

## 3. Telas

- [x] 3.1 Portas de entrada: marca no topo, formulário em cartão, boas-vindas com a marca grande
- [x] 3.2 Área do cliente: casa, agenda, loja e pedidos com `topo_do_cliente`; tirar os botões de navegação da casa (D4); espécie em coral (D5) — o `_topo` da loja saiu
- [x] 3.3 Área da clínica: topo com a marca e menu em pílulas

## 4. Verificação

- [x] 4.1 `python -m unittest discover -s tests` — **59 testes, OK** (o projeto usa `unittest`, não `pytest`)
- [x] 4.2 Ver no navegador, em claro e escuro, as portas de entrada, as quatro telas do cliente e três da clínica; navegar pelo cabeçalho e conferir o destaque — **Visto em 19/10:** boas-vindas em escuro e entrar em claro, com a marca, a Nunito carregada (`document.fonts.check`) e o degradê; como tutora (Ana), casa com os três animais e espécie em coral, e o clique em **Loja** no cabeçalho levou a `/loja` com a pílula Loja destacada; agenda e meus pedidos com o mesmo cabeçalho e o destaque certo; como equipe (Carla), painel, **Serviços** pela pílula (destacada, em escuro) e Animais com as espécies em coral.
      De passagem: o console tinha seis `removeChild` do React num `<link>`, deixados pelo hot reload durante as edições — não voltaram depois de recarregar a página
- [x] 4.3 `openspec validate identidade-visual --strict`
