// Lista pet.
// O tutor recebe so as linhas em que id_cliente e a ficha dele.
query pet verb=GET {
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
        db.query pet {
          sort = {nome: "asc"}
          return = {type: "list"}
        } as $todos

        var.update $registros {
          value = $todos
        }
      }
      else {
        db.query pet {
          where = $db.pet.id_cliente == $ctx.cliente_id
          sort = {nome: "asc"}
          return = {type: "list"}
        } as $meus

        var.update $registros {
          value = $meus
        }
      }
    }
  }

  response = $registros
}
