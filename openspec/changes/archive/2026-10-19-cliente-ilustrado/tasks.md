## 1. Ilustrações

- [x] 1.1 SVGs em `assets/ilustracoes/`: `cao`, `gato`, `outro`, `banner`, `vazio-animais`, `vazio-pedidos`, `vazio-agenda` e `produto-<categoria>` para as seis categorias mais `produto-outro` (D1) — 14 arquivos, servidos como `image/svg+xml`
- [x] 1.2 `petbits/ilustracoes.py` com `imagem_da_especie` e `imagem_da_categoria` (D2), e `tests/test_ilustracoes.py` — 6 testes, inclusive um que confere que todo arquivo que as funções podem devolver existe em `assets/`

## 2. Casa

- [x] 2.1 `PetState` acrescenta `imagem` a cada animal; cartão com o avatar
- [x] 2.2 Banner de boas-vindas com ilustração, saudação e atalhos (D3) — a ilustração some abaixo de `sm`
- [x] 2.3 Casa sem animal com `tela_vazia` (D4); aviso de `<div>` em `<p>` corrigido (D5)

## 3. Loja, pedidos e agenda

- [x] 3.1 `LojaState` acrescenta `imagem` a cada produto; cartão com a imagem no topo
- [x] 3.2 Meus pedidos e Meus agendamentos vazios com `tela_vazia` — o "Marcar agora" rola até o formulário (`rx.scroll_to("marcar")`)

## 4. Verificação

- [x] 4.1 `python -m unittest discover -s tests` sem falha — **65 testes, OK**
- [x] 4.2 No navegador como tutora: casa, loja e as três telas vazias, em claro, escuro e celular; console sem erro novo — **Visto em 19/10:** como Ana, banner com "Olá, Ana!" e os dois atalhos, Mel ("Cachorro") com o cão e Nina e Tomate ("Gato") com o gato; a loja com as 17 imagens carregadas de `/ilustracoes/`, cada uma da sua categoria. Como cliente novo (criado por `criar_clientes_de_teste.py 1`), as três telas vazias: casinha, sacola com botão para a loja, calendário com "Marcar agora", que levou a página ao formulário. Celular claro sem rolagem lateral, a ilustração do banner escondida. Sem o aviso de `<div>` em `<p>` no console.
      **Defeito achado e corrigido na verificação:** com a lista de agendamentos recusada pelo Xano (429), a tela vazia aparecia junto com o erro — contra o requisito "Telas vazias ilustradas". Agora agenda e pedidos só mostram a tela vazia sem erro; visto o caso sem erro depois da correção. O caso com erro ficou provado pelo código (`rx.cond` sobre `erro_lista` e `erro`), não reproduzido de novo — forçar outro 429 seria gastar a cota da instância de propósito
- [x] 4.3 `openspec validate cliente-ilustrado --strict`
