// Foto de um produto da loja, enviada pela equipe (change `foto-do-produto`,
// D2 e D6).
//
// Molde do `pet/{pet_id}/foto`, com a abertura de equipe no lugar da prova de
// posse: `produto` nao tem dono, entao a recusa de cliente e o
// `PetBits/exige_equipe`, antes de qualquer `db.*` e antes de guardar o
// arquivo. Sem transacao com trava: la ela protege a posse, e aqui nao ha
// dono nem produto apagado (desativar e `ativo = false`).
query "equipe/produtos/{produto_id}/foto" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Grava a foto de um produto da loja"

  input {
    int produto_id filters=min:1
    file? foto
    text extensao filters=trim|lower
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    precondition ($input.foto != null) {
      error_type = "inputerror"
      error = "Envie uma imagem."
    }

    // O produto e conferido ANTES de guardar o arquivo: um id errado nao
    // deixa imagem orfa no armazenamento.
    db.query produto {
      where = $db.produto.id == $input.produto_id
      output = ["id"]
      return = {type: "single"}
    } as $existente

    precondition ($existente != null) {
      error_type = "notfound"
      error = "Produto nao encontrado."
    }

    // MEDIDO na `perfil-e-fotos`: o `storage.create_image` exige a extensao
    // no `filename`, e o nome original nao chega pelo input. A extensao vem
    // em campo proprio, de lista fechada -- `in`, e nao `contains`, que e de
    // texto.
    precondition ((["jpg", "jpeg", "png", "webp"]|in:$input.extensao) == true) {
      error_type = "inputerror"
      error = "A foto precisa ser JPG, PNG ou WebP."
    }

    var $imagem {
      value = null
    }

    // Conteudo que nao e imagem (um PDF renomeado para .jpg) faz o
    // `storage.create_image` lancar; o catch transforma isso em 400.
    try_catch {
      try {
        storage.create_image {
          value = $input.foto
          access = "public"
          filename = "produto." ~ $input.extensao
        } as $guardada

        var.update $imagem {
          value = $guardada
        }
      }

      catch {
        precondition (false) {
          error_type = "inputerror"
          error = "O arquivo enviado nao e uma imagem valida."
        }
      }
    }

    precondition ((["image/jpeg", "image/png", "image/webp"]|in:$imagem.mime) == true) {
      error_type = "inputerror"
      error = "A foto precisa ser JPG, PNG ou WebP."
    }

    precondition ($imagem.size <= 5242880) {
      error_type = "inputerror"
      error = "A foto pode ter no maximo 5 MB."
    }

    db.patch produto {
      field_name = "id"
      field_value = $existente.id
      data = {foto: $imagem}
    } as $atualizado
  }

  response = {id: $atualizado.id, foto: $atualizado.foto}
}
