// Lista funcionario. O tutor recebe so id, nome e cargo -- a ficha
// tem CPF, telefone e e-mail, que nao sao informacao de cliente.
query funcionario verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    var $registros {
      value = []
    }

    conditional {
      if ($ctx.is_admin == true) {
        db.query funcionario {
          sort = {nome: "asc"}
          return = {type: "list"}
        } as $todos

        var.update $registros {
          value = $todos
        }
      }
      else {
        db.query funcionario {
          sort = {nome: "asc"}
          output = ["id", "nome", "cargo"]
          return = {type: "list"}
        } as $publico

        var.update $registros {
          value = $publico
        }
      }
    }
  }

  response = $registros
}
