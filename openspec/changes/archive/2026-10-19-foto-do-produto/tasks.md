## 1. Medição

- [x] 1.1 Medir se abrir URLs públicas de foto do Xano conta no limite de 10 requisições a cada 20 s: carregar 12 fotos já gravadas em sequência e, logo depois, chamar a API; anotar o resultado aqui — **Medido em 19/10:** com a janela limpa, 12 GETs seguidos às URLs públicas de foto (o host é o da instância, que responde 303 e redireciona para `storage.googleapis.com`) e logo depois 9 chamadas à API: as 9 deram 200. Somando 21 pedidos ao host em menos de 20 s, as fotos não contam no limite

## 2. Tabela

- [x] 2.1 `image? foto` em `tables/produto.xs` (D1); validar; prévia do `publicar.py` mostrando só a coluna nova; publicar — a prévia mostrou `UPDATE`/`ADD_FIELD` em `produto` e nada mais

## 3. Endpoints

- [x] 3.1 `apis/pet_bits/equipe_produto_foto.xs` — `POST equipe/produtos/{produto_id}/foto` na ordem do D2
- [x] 3.2 `foto` no `output` de `equipe_produto_list.xs` e `loja_produtos.xs` (D3)
- [x] 3.3 Validar, prévia e publicar os três; `verificar_equipe.py` limpo — prévia: `CREATE` do POST e `UPDATE` das duas listas; a guarda passou de 20 para 21 endpoints de equipe, nenhuma acusação

## 4. Reflex

- [x] 4.1 `imagem_do_produto(nome, categoria, foto=None)` com a foto enviada na frente (D4), e teste da ordem em `tests/test_ilustracoes.py`
- [x] 4.2 `xano.enviar_foto_do_produto` com o `_arquivo_de_foto` que já existe
- [x] 4.3 `LojaState.carregar_loja` passa a foto para `imagem_do_produto`
- [x] 4.4 `EquipeState`: imagem no item do catálogo, `enviar_foto_produto` com a conferência de `fotos_enviadas`; `pages/equipe.py`: imagem no cartão e foto no diálogo de edição (D5)

## 5. Docs

- [x] 5.1 `docs/domain-model.md`: foto entre as informações do Produto; `docs/project-overview.md`: foto de produto enviada pela equipe no escopo

## 6. Verificação

- [x] 6.1 Contra o Xano: as provas do design, com conta de equipe e com conta de cliente — **Feito em 19/10** na "Escova removedora de pelos" (id 19): WebP da equipe → 200 com URL pública; troca por PNG → 200 e a URL mudou; PDF → 400 "A foto precisa ser JPG, PNG ou WebP."; `.jpg` que não é imagem → 400 "O arquivo enviado nao e uma imagem valida."; PNG de 5,5 MB → 400 "A foto pode ter no maximo 5 MB."; `produto_id` 999999 → 404 "Produto nao encontrado."; **conta de cliente → 403 "Sem permissao para esta area."**; depois das recusas, `equipe/produtos` e `loja/produtos` traziam a mesma URL da troca (nada foi sobrescrito), e a loja traz `foto` em todos os itens. A escova ficou com a própria foto, enviada pela equipe.
      **Achado:** o `storage.create_image` do plano gratuito grava a imagem com a marca "Powered by Xano / Nocode backend" no canto inferior esquerdo (o arquivo baixado tem 108 KB contra 63 KB do original). Vale também para as fotos de tutor e animal da `perfil-e-fotos`. Fica registrado para decisão, fora desta change
- [x] 6.2 Navegador: equipe envia e troca a foto; loja e detalhe mostram; produto sem foto enviada igual a antes; claro, escuro e celular — **Visto em 19/10:** como Carla, `/equipe/produtos` mostra a imagem em cada cartão (a da escova vinda do Xano, as outras de `/fotos/`); no diálogo da escova, "Trocar foto" e "Foto enviada pela equipe."; PDF e arquivo de 6 MB mostraram os avisos sem enviar; a WebP trocou a imagem do diálogo e do cartão na hora, sem recarregar; a "Areia higiênica" mostra "Escolher foto" e "Foto automática."; o "Novo produto" mostra "Depois de cadastrar, edite o produto para pôr a foto dele." e nenhum seletor. Como Ana, a loja e o detalhe da escova mostram a foto enviada e os outros produtos as de antes. Escuro no computador, claro no celular (375 px) sem rolagem lateral. A escolha de arquivo foi simulada pelo `input` do seletor, porque o navegador embutido não abre a janela de arquivos
- [x] 6.3 `unittest`, `verificar_equipe.py`, `openspec validate foto-do-produto --strict` — **83 testes, OK**; `verificar_equipe.py`: 21 endpoints de equipe, nenhuma acusação; os 42 `.xs` válidos; `publicar.py --conferir` sem nada do repositório faltando no Xano
