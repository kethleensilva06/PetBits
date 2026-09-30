// Lista pedido.
// O tutor recebe so as linhas em que id_cliente e a ficha dele.
query pedido verb=GET {
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
        db.query pedido {
          sort = {data_pedido: "desc"}
          return = {type: "list"}
        } as $todos

        var.update $registros {
          value = $todos
        }
      }
      else {
        db.query pedido {
          where = $db.pedido.id_cliente == $ctx.cliente_id
          sort = {data_pedido: "desc"}
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
