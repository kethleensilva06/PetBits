// Foto de perfil do tutor (change `perfil-e-fotos`, D2 e D3).
//
// O Reflex confere tipo e tamanho antes de enviar, mas quem decide e este
// endpoint: depois de guardar, confere o `mime` e o `size` do que recebeu, e
// so entao grava na ficha. Uma foto recusada fica no armazenamento sem ficha
// que aponte para ela -- pequena, rara e nao exposta (design.md, D2).
//
// Acesso `public`: URL assinada custaria uma requisicao a mais por exibicao
// (design.md, D3).
query "me/tutor/foto" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Grava a foto de perfil do tutor autenticado"

  input {
    file? foto
    text extensao filters=trim|lower
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    precondition ($input.foto != null) {
      error_type = "inputerror"
      error = "Envie uma imagem."
    }

    // A ficha e conferida ANTES de guardar o arquivo: conta sem ficha nao
    // chega a deixar imagem no armazenamento.
    db.query tutor {
      where = $db.tutor.id_user == $auth.id
      output = ["id"]
      return = {type: "single"}
    } as $previa

    precondition ($previa != null) {
      error_type = "accessdenied"
      error = "Esta conta nao tem ficha de tutor."
    }

    // MEDIDO: `storage.create_image` tira a extensao do `filename`, e sem
    // ela recusa com ERROR_FATAL (500) "Invalid file extension.". O nome
    // original do arquivo NAO chega acessivel pelo input (`foto.name` da
    // "Unable to locate input"), entao a extensao vem como campo proprio, de
    // uma lista fechada -- conferida aqui, para a recusa sair como 400.
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
          filename = "perfil." ~ $input.extensao
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

    db.transaction {
      stack {
        db.query tutor {
          where = $db.tutor.id_user == $auth.id
          lock = true
          output = ["id"]
          return = {type: "single"}
        } as $minha

        precondition ($minha != null) {
          error_type = "accessdenied"
          error = "Esta conta nao tem ficha de tutor."
        }

        db.patch tutor {
          field_name = "id"
          field_value = $minha.id
          data = {foto: $imagem}
        } as $atualizada
      }
    }
  }

  response = {foto: $atualizada.foto}
}
