## 1. Medição

- [x] 1.1 Medir se `file? image` na entrada já recusa arquivo que não é imagem, e o que `storage.create_image` devolve em `mime`, `size` e `url` (D2) — **Medido em 19/10, três achados:** (1) `storage.create_image` tira a extensão do `filename` e, sem ela, recusa com ERROR_FATAL 500 "Invalid file extension."; (2) o nome original do arquivo **não** chega pelo `input` (`$input.foto.name` dá "Unable to locate input"), então a extensão vai num campo próprio, `extensao`, de lista fechada; (3) conteúdo que não é imagem com nome `.jpg` faz o `create_image` lançar, e um `try_catch` transforma isso em 400. A resposta traz `access`, `path`, `name`, `type`, `size`, `mime`, `meta` (largura e altura) e `url` pública. De passagem: para lista o filtro é `in`; `contains` é de texto e recusava até o WebP

## 2. Tabelas

- [x] 2.1 `image? foto` em `tables/tutor.xs` e `tables/pet.xs` (D1); validar; `--dry-run` mostrando só a coluna nova; publicar — a prévia mostrou `ADD_FIELD` nas duas tabelas e nada mais

## 3. Endpoints

- [x] 3.1 `PATCH me/tutor` (D4)
- [x] 3.2 `POST me/senha` (D5)
- [x] 3.3 `POST me/tutor/foto` e `POST pet/{pet_id}/foto`, com posse provada pelo token e conferência de tipo e tamanho (D2, D3) — a ficha e a posse são conferidas **antes** de guardar o arquivo, e a extensão antes do `create_image`
- [x] 3.4 `GET pets` inclui `foto` no `output` (D7); publicar os endpoints com `--dry-run` antes

## 4. Reflex

- [x] 4.1 Cliente HTTP em `petbits/xano.py` (JSON e multipart)
- [x] 4.2 `/perfil` com `PerfilState`: dados, CPF e e-mail travados, troca de senha, foto
- [x] 4.3 Avatar no `topo_do_cliente` levando a `/perfil`; foto guardada no `AuthState` (D6); `sair` limpa
- [x] 4.4 Foto do animal no diálogo e no cartão (D7)
- [x] 4.5 `petbits/fotos_enviadas.py`: conferência de extensão e tamanho antes de enviar, com o motivo em português. O seletor **não** filtra por tipo: com `accept` e `max_size` no `rx.upload`, o arquivo recusado sumia sem aviso nenhum — nem o `on_drop_rejected` chegou ao State na medição —, e a pessoa clicaria sem resposta

## 5. Docs

- [x] 5.1 `docs/project-overview.md`: foto de perfil no escopo; prontuário com imagem continua fora

## 6. Verificação

- [x] 6.1 Contra o Xano: as provas do design, incluindo as recusas — **Feito em 19/10 com as contas de teste:** `PATCH me/tutor` com telefone, `documento` e `email` mudou só o telefone (CPF e e-mail iguais), e o telefone voltou ao original; nome em branco → 400; senha atual errada → 400 "A senha atual nao confere."; nova senha de 3 caracteres → 400 da coluna; troca certa de ponta a ponta: com a temporária a original é recusada e a temporária entra, e a conta voltou à senha original do arquivo de contas de teste (conferido entrando com ela); foto WebP aceita, com URL pública na ficha e na lista; PDF → 400 pela extensão; `.jpg` que não é imagem → 400 "O arquivo enviado nao e uma imagem valida."; PNG de 6,2 MB → 400 pelo limite; foto no animal de **outro** tutor → 404 "Animal nao encontrado." e o animal dele continuou sem foto; `pet_id` inexistente → o mesmo 404.
      Para a prova do animal alheio foi preciso criar um animal ("Teste foto alheia") numa conta de cliente de teste que não tinha nenhum. Ficaram de dado de teste: a foto de perfil da Ana (um coelho) e as fotos da Mel e do Tomate
- [x] 6.2 Navegador: perfil, senha, foto do tutor e do animal; claro, escuro e celular — **Visto em 19/10 como Ana:** tocar no avatar do cabeçalho abriu `/perfil`; nome, telefone e endereço livres, CPF e e-mail travados; telefone alterado e salvo, "Dados atualizados.", igual depois de recarregar, e devolvido; senha atual errada mostrou a recusa; foto trocada pelo seletor, e o avatar do cabeçalho mudou junto; PDF e arquivo de 6 MB mostraram "A foto precisa ser JPG, PNG ou WebP." e "A foto pode ter no máximo 5 MB."; no diálogo de editar o Tomate, "Escolher foto" enviou a foto, o botão virou "Trocar foto" e o cartão mostra a foto depois de recarregar, enquanto a Nina, sem foto, mantém a da espécie; perfil no celular e escuro sem rolagem lateral; "Sair" apagou a foto e o token do armazenamento local, e `/perfil` sem sessão levou a `/entrar`.
      Um defeito apareceu e foi corrigido: o aviso de erro da foto de uma visita anterior continuava na tela ao voltar ao perfil; o `carregar` passou a limpar os avisos
- [x] 6.3 `unittest`, `verificar_equipe.py`, `openspec validate perfil-e-fotos --strict` — **81 testes, OK**; `verificar_equipe.py`: 20 endpoints de equipe, nenhuma acusação
