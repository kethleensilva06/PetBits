// Foto do animal, enviada pelo dono (change `perfil-e-fotos`, D2, D3 e D7).
//
// A posse e provada como no `pet/{pet_id}` PATCH: consulta-prova com join e
// `where` por id E dono, com lock, e `db.patch` pelo id da prova -- nunca pelo
// id da requisicao. Animal de outro tutor sai igual a animal inexistente.
query "pet/{pet_id}/foto" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Grava a foto de um animal do tutor autenticado"

  input {
    int pet_id filters=min:1
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

    // A prova de posse vem ANTES de guardar o arquivo: quem tenta o pet_id
    // alheio nao chega a deixar imagem nenhuma no armazenamento.
    db.query pet {
      join = {
        tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
      }

      where = ($db.pet.id == $input.pet_id) && ($db.tutor.id_user == $auth.id)
      output = ["id"]
      return = {type: "single"}
    } as $previa

    precondition ($previa != null) {
      error_type = "notfound"
      error = "Animal nao encontrado."
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
          filename = "animal." ~ $input.extensao
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
        db.query pet {
          join = {
            tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
          }

          where = ($db.pet.id == $input.pet_id) && ($db.tutor.id_user == $auth.id)
          lock = true
          output = ["id"]
          return = {type: "single"}
        } as $meu

        precondition ($meu != null) {
          error_type = "notfound"
          error = "Animal nao encontrado."
        }

        db.patch pet {
          field_name = "id"
          field_value = $meu.id
          data = {foto: $imagem}
        } as $atualizado
      }
    }
  }

  response = {id: $atualizado.id, foto: $atualizado.foto}
}
