// Busca um funcionario pelo id. O tutor recebe so id, nome e cargo.
query "funcionario/{id}" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
    // Identificador do registro
    int id
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    var $registro {
      value = null
    }

    conditional {
      if ($ctx.is_admin == true) {
        db.get funcionario {
          field_name = "id"
          field_value = $input.id
        } as $completo

        var.update $registro {
          value = $completo
        }
      }
      else {
        db.get funcionario {
          field_name = "id"
          field_value = $input.id
          output = ["id", "nome", "cargo"]
        } as $publico

        var.update $registro {
          value = $publico
        }
      }
    }
  }

  response = $registro
}
