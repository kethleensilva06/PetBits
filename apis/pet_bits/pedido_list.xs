// Os pedidos do tutor autenticado, com os itens (change `loja`, D5).
//
// Duas consultas, as duas nascendo filtradas pelo join ate a conta do token
// -- o padrao de leitura da change `animais-do-tutor`. Nao existe instante
// em que um pedido alheio esteja numa variavel deste endpoint. O Python
// agrupa os itens por pedido.
query pedidos verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista os pedidos do tutor autenticado, com os itens"

  input {
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.query pedido {
      join = {
        tutor: {type: "inner", table: "tutor", where: $db.pedido.id_tutor == $db.tutor.id}
      }

      where = $db.tutor.id_user == $auth.id
      sort = {created_at: "desc"}
      output = ["id", "created_at", "situacao", "forma_pagamento", "entrega", "endereco_entrega", "total", "pago_em"]
      return = {type: "list"}
    } as $pedidos

    db.query pedido_item {
      join = {
        pedido: {type: "inner", table: "pedido", where: $db.pedido_item.id_pedido == $db.pedido.id}
        tutor : {type: "inner", table: "tutor", where: $db.pedido.id_tutor == $db.tutor.id}
      }

      where = $db.tutor.id_user == $auth.id
      output = ["id_pedido", "produto_nome", "quantidade", "preco_unitario", "valor_linha"]
      return = {type: "list"}
    } as $itens
  }

  response = {pedidos: $pedidos, itens: $itens}
}
