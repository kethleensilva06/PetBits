// Foto do colaborador, enviada por ele mesmo (change `perfil-do-colaborador`, D5).
//
// O upload repete o do `me/tutor/foto` com as medicoes da `perfil-e-fotos`:
// a extensao vem em campo proprio, de lista fechada (o nome original nao chega
// pelo input, e o `storage.create_image` exige a extensao no nome); conteudo
// que nao e imagem cai no `try_catch` como 400; tipo e tamanho conferidos
// depois de guardar. A ficha e a do e-mail da conta do token (D1), conferida
// ANTES de guardar o arquivo.
query "equipe/meu-perfil/foto" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Grava a foto da ficha de colaborador da conta de equipe"

  input {
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

    db.get user {
      field_name = "id"
      field_value = $id_conta
      output = ["id", "email"]
    } as $conta

    db.query colaborador {
      where = $db.colaborador.email == $conta.email
      output = ["id"]
      return = {type: "list"}
    } as $previa

    precondition (($previa|count) == 1) {
      error_type = "accessdenied"
      error = "Nao ha uma ficha de colaborador com o seu e-mail. Procure a gerencia."
    }

    precondition ((["jpg", "jpeg", "png", "webp"]|in:$input.extensao) == true) {
      error_type = "inputerror"
      error = "A foto precisa ser JPG, PNG ou WebP."
    }

    var $imagem {
      value = null
    }

    try_catch {
      try {
        storage.create_image {
          value = $input.foto
          access = "public"
          filename = "colaborador." ~ $input.extensao
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
        db.query colaborador {
          where = $db.colaborador.email == $conta.email
          lock = true
          output = ["id"]
          return = {type: "list"}
        } as $fichas

        precondition (($fichas|count) == 1) {
          error_type = "accessdenied"
          error = "Nao ha uma ficha de colaborador com o seu e-mail. Procure a gerencia."
        }

        var $minha {
          value = $fichas|first
        }

        db.patch colaborador {
          field_name = "id"
          field_value = $minha.id
          data = {foto: $imagem}
        } as $atualizada
      }
    }
  }

  response = {foto: $atualizada.foto}
}
