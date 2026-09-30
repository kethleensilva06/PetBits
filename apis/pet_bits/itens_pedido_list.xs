// Lista itens_pedido.
// O dono de itens_pedido esta a um salto: o filtro entra como join, para
// o recorte acontecer no banco e nao depois de baixar a tabela toda.
query itens_pedido verb=GET {
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
        db.query itens_pedido {
          sort = {id: "asc"}
          return = {type: "list"}
        } as $todos

        var.update $registros {
          value = $todos
        }
      }
      else {
        db.query itens_pedido {
          join = {
            pedido: {table: "pedido", where: $db.itens_pedido.id_pedido == $db.pedido.id}
          }

          where = $db.pedido.id_cliente == $ctx.cliente_id
          sort = {id: "asc"}
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
