## 1. Mensagens e avisos

- [x] 1.1 `petbits/mensagens.py` e `_detalhe` em `petbits/xano.py` (D1); `tests/test_mensagens.py` — o teste lê as 69 mensagens dos `.xs` e confere que nenhuma fica com palavra sem acento da tabela; a primeira rodada achou "disponivel", "area", "esta incompleto" e "a venda", que entraram na tabela
- [x] 1.2 Perfil: confirmações em `rx.toast` (D2) — dados, senha e foto, nos dois perfis; e "N no carrinho." ao adicionar pelo detalhe

## 2. Menu da clínica

- [x] 2.1 Menu de celular e topo enxuto (D3) — o "Sair" do cabeçalho virou só ícone no celular, nas duas áreas (com `aria_label`), e o selo "Tutor" também some no celular

## 3. Loja

- [x] 3.1 Busca e filtro (D4) — `filtrar_produtos` é função pura, testada
- [x] 3.2 Quantidade no detalhe e carrinho no cabeçalho (D4)

## 4. Máscaras

- [x] 4.1 `petbits/mascaras.py` e `tests/test_mascaras.py`; cadastro, balcão, colaboradores e perfis (D5) — o CPF do perfil (travado) também aparece formatado

## 5. Verificação de ponta a ponta

- [x] 5.1 `finally` que desativa o produto (D6) — e um teste novo em `tests/test_ponta_a_ponta.py`: uma rodada que cai no meio (erro em `meus_pedidos`) deixa o produto de verificação inativo

## 6. Verificação

- [x] 6.1 Suíte toda — **93 testes, OK**
- [x] 6.2 Navegador, como descrito no design — **Visto em 19/10:** como Carla, no celular, o topo coube numa linha (marca, avatar, ícone de sair) e as 9 abas viraram o botão "☰ Serviços"; tocar abriu as 9 áreas com Serviços destacada, e tocar em Agenda levou a `/equipe/agenda`; na tela larga, as 9 abas e nenhum botão. Senha atual errada no perfil mostrou "A senha atual não confere.". Como Ana, a busca "racao" deixou só as três rações, "xyzw" mostrou "Nenhum produto encontrado com essa busca." com o botão de limpar, e o filtro Brinquedo deixou só os três brinquedos; no detalhe da Bolinha, + duas vezes deu 3, "Adicionar" pôs 3 no carrinho, o detalhe mostrou "No carrinho: 3", o ícone do cabeçalho mostrou 3 e apareceu "3 no carrinho."; no perfil, o telefone veio formatado, digitar `11977776666` virou `(11) 97777-6666`, o CPF travado aparece `123.456.789-01`, salvar mostrou "Dados atualizados." numa notificação que sumiu sozinha em menos de 8 s (sem texto fixo na tela), e o telefone voltou ao original; no cadastro, digitar `12345678909` virou `123.456.789-09` (nada foi enviado).
      Um defeito apareceu e foi corrigido: o menu do celular abria com 812 px de altura e o degradê da página, porque o Radix marca cada menu flutuante com `.radix-themes` e a regra de fundo e altura do `assets/estilo.css` valia para ele; a regra passou a ser `body > .radix-themes`, e o menu ficou com 304 px
- [x] 6.3 `openspec validate acabamentos-de-tela --strict`
