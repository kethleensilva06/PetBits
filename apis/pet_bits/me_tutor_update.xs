// O tutor altera os proprios dados de contato (change `perfil-e-fotos`, D4).
//
// Mesmo modelo de escrita do `pet/{pet_id}` PATCH: corpo cru + `pick`, para
// campo ausente nao virar "" e apagar o que estava la; consulta-prova com
// lock dentro de transacao; `db.patch` pelo id que a PROVA devolveu.
//
// `documento` e `email` NEM ESTAO no `input`: nao existem em `$input`, entao
// o `pick` nao tem como coloca-los em `$dados`. CPF identifica a pessoa e o
// e-mail e o login -- os dois continuam pela clinica.
query "me/tutor" verb=PATCH {
  api_group = "PetBits"
  auth = "user"
  description = "Altera nome, telefone e endereco da ficha do tutor autenticado"

  input {
    text nome? filters=trim
    text telefone? filters=trim
    text endereco? filters=trim
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $corpo_cru

    var $dados {
      value = `$input|pick:($corpo_cru|keys)`
    }

    precondition (($dados|count) > 0) {
      error_type = "inputerror"
      error = "Informe ao menos um campo para alterar."
    }

    conditional {
      if (($dados|has:"nome") == true) {
        precondition ((($dados|get:"nome")|trim) != "") {
          error_type = "inputerror"
          error = "O nome nao pode ficar em branco."
        }
      }
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
          data = $dados
        } as $atualizada

        // A saudacao vem do nome da CONTA (`auth/me`), nao da ficha. Sem isto,
        // o nome novo valia so ate sair, e o antigo voltava na entrada
        // seguinte (change `perfil-do-colaborador`, D4).
        conditional {
          if (($dados|has:"nome") == true) {
            db.edit user {
              field_name = "id"
              field_value = $auth.id
              data = {name: $dados|get:"nome"}
            } as $conta_editada
          }
        }
      }
    }
  }

  response = {
    id       : $atualizada.id
    nome     : $atualizada.nome
    documento: $atualizada.documento
    email    : $atualizada.email
    telefone : $atualizada.telefone
    endereco : $atualizada.endereco
    foto     : $atualizada.foto
  }
}
