## Decisions

### D1. Remover é gravar `foto` vazia

`DELETE equipe/produtos/{produto_id}/foto` grava `foto = null`. A loja já
escolhe a imagem nesta ordem: foto enviada, foto do produto que acompanha o
app, foto da categoria (`imagem_do_produto`). Sem foto enviada, o produto volta
sozinho para a automática. O arquivo antigo fica no armazenamento do Xano; o
plano gratuito não tem lixo a esvaziar por aqui.

### D2. Foto no cadastro, enviada depois de salvar

A foto é gravada pelo id do produto, que só existe depois do cadastro. O
arquivo escolhido fica guardado no servidor do Reflex (`_foto_pendente`, que
não vai ao navegador), com uma prévia no formulário; ao salvar, o cadastro
devolve o id e a foto é enviada em seguida. Se a foto falhar, o produto fica
cadastrado com a foto automática e o erro aparece.

### D3. Mesmo lugar para trocar

A miniatura do cartão abre a edição do produto, onde a foto já mora, em vez de
uma tela nova para a mesma coisa.
