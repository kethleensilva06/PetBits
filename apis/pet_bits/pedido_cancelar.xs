// Cancela um pedido do tutor autenticado, enquanto aguarda pagamento (change
// `cliente-cancela-pedido`).
//
// Posse pelo join, sob trava, como em `agendamento_cancelar.xs` (D1): pedido
// alheio e pedido inexistente respondem igual, "nao encontrado". So `pendente`
// e sem pagamento registrado (D2): depois disso, desfazer envolve a clinica.
//
// Cancelar devolve o estoque de cada item na MESMA transacao (D3), com o mesmo
// laco do `equipe_pedido_situacao.xs`: ou tudo volta, ou nada muda.
query "pedido/{pedido_id}/cancelar" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cancela um pedido do tutor autenticado enquanto aguarda pagamento"

  input {
    int pedido_id filters=min:1
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.transaction {
      stack {
        db.query pedido {
          join = {
            tutor: {type: "inner", table: "tutor", where: $db.pedido.id_tutor == $db.tutor.id}
          }

          where = ($db.pedido.id == $input.pedido_id) && ($db.tutor.id_user == $auth.id)
          lock = true
          output = ["id", "situacao", "pago_em"]
          return = {type: "single"}
        } as $meu

        precondition ($meu != null) {
          error_type = "notfound"
          error = "Pedido nao encontrado."
        }

        precondition ($meu.situacao == "pendente") {
          error_type = "inputerror"
          error = "Este pedido nao pode mais ser cancelado. Fale com a clinica."
        }

        precondition (($meu.pago_em == null) || ($meu.pago_em == 0)) {
          error_type = "inputerror"
          error = "Este pedido nao pode mais ser cancelado. Fale com a clinica."
        }

        db.query pedido_item {
          where = $db.pedido_item.id_pedido == $meu.id
          output = ["id_produto", "quantidade"]
          return = {type: "list"}
        } as $itens

        foreach ($itens) {
          each as $item {
            db.query produto {
              where = $db.produto.id == $item.id_produto
              lock = true
              output = ["id", "estoque"]
              return = {type: "single"}
            } as $produto

            conditional {
              if ($produto != null) {
                db.patch produto {
                  field_name = "id"
                  field_value = $produto.id
                  data = {estoque: $produto.estoque + $item.quantidade}
                } as $devolvido
              }
            }
          }
        }

        db.patch pedido {
          field_name = "id"
          field_value = $meu.id
          data = {situacao: "cancelado"}
        } as $cancelado
      }
    }
  }

  response = {id: $cancelado.id, situacao: $cancelado.situacao}
}
