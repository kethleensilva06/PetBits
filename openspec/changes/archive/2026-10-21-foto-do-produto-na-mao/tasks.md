## 1. Backend

- [x] 1.1 `equipe_produto_foto_remover.xs`; validar, publicar e provar (cliente recusado, remoção de verdade)

## 2. Tela

- [x] 2.1 `xano.remover_foto_do_produto`; `EquipeState.remover_foto_produto`
- [x] 2.2 Foto escolhida no cadastro (`_foto_pendente`), enviada depois de salvar
- [x] 2.3 Miniatura do cartão abre a edição; Remover foto na edição

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador, como equipe: trocar, remover e cadastrar com foto

Medido no Xano, com a Areia higiênica (11), que não tinha foto enviada: uma foto
de teste foi enviada; a conta de cliente foi recusada ao remover; a equipe
removeu e o produto voltou a ficar sem foto. Na tela, como Carla: a miniatura
do cartão abriu a edição; a foto escolhida foi enviada, apareceu no cartão, e
Remover foto voltou a prévia e o cartão para `/fotos/produtos/areia-higienica.webp`.
Ao fim, o produto está como antes. O cadastro com foto não foi feito na tela,
para não deixar um produto de teste permanente na lista da clínica: está
coberto por `tests/test_foto_do_produto_na_mao.py` (a foto vai com o id do
produto novo; sem foto, nada é enviado).
