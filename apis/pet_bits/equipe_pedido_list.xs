// Os pedidos da loja, de todos os clientes, para a equipe (change
// `pedidos-da-equipe`, D1). Filtro opcional por situacao.
//
// Abertura de equipe conferida pela guarda `verificar_equipe.py`: `pedido`
// tem dono, mas esta consulta e de proposito SEM filtro de dono -- e a prova
// de equipe que a protege.
query "equipe/pedidos" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista os pedidos da loja, com itens, para a equipe"

  input {
    // Vazio traz todos.
    text situacao? filters=trim
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

    var $pedidos {
      value = []
    }

    var $itens {
      value = []
    }

    conditional {
      if (($input.situacao == null) || ($input.situacao == "")) {
        db.query pedido {
          join = {
            tutor: {type: "left", table: "tutor", where: $db.pedido.id_tutor == $db.tutor.id}
          }

          eval = {cliente_nome: $db.tutor.nome, cliente_telefone: $db.tutor.telefone}
          sort = {created_at: "desc"}
          output = ["id", "created_at", "situacao", "forma_pagamento", "entrega", "endereco_entrega", "total", "pago_em", "origem", "cliente_nome", "cliente_telefone"]
          return = {type: "list"}
        } as $todos

        db.query pedido_item {
          output = ["id_pedido", "produto_nome", "quantidade", "preco_unitario", "valor_linha"]
          return = {type: "list"}
        } as $todos_itens

        var.update $pedidos {
          value = $todos
        }

        var.update $itens {
          value = $todos_itens
        }
      }

      else {
        db.query pedido {
          join = {
            tutor: {type: "left", table: "tutor", where: $db.pedido.id_tutor == $db.tutor.id}
          }

          where = $db.pedido.situacao == $input.situacao
          eval = {cliente_nome: $db.tutor.nome, cliente_telefone: $db.tutor.telefone}
          sort = {created_at: "desc"}
          output = ["id", "created_at", "situacao", "forma_pagamento", "entrega", "endereco_entrega", "total", "pago_em", "origem", "cliente_nome", "cliente_telefone"]
          return = {type: "list"}
        } as $filtrados

        db.query pedido_item {
          join = {
            pedido: {type: "inner", table: "pedido", where: $db.pedido_item.id_pedido == $db.pedido.id}
          }

          where = $db.pedido.situacao == $input.situacao
          output = ["id_pedido", "produto_nome", "quantidade", "preco_unitario", "valor_linha"]
          return = {type: "list"}
        } as $filtrados_itens

        var.update $pedidos {
          value = $filtrados
        }

        var.update $itens {
          value = $filtrados_itens
        }
      }
    }
  }

  response = {pedidos: $pedidos, itens: $itens}
}
