// A regra de estoque da loja, num lugar so (change `venda-no-balcao`, D1).
//
// Usada pelo `POST pedidos` (site) e pelo `POST equipe/vendas` (balcao). Cada
// um valida o que e seu -- dono, entrega, endereco, prova de equipe -- e chama
// esta funcao com o resto ja decidido.
//
// NAO recebe preco nem total: so produto e quantidade de cada item. O preco
// vem do catalogo e e congelado no item; a linha e o total sao calculados
// aqui. Tudo numa transacao: para cada item, o produto e lido com TRAVA, o
// estoque e conferido e baixado; qualquer recusa no meio desfaz o que ja
// tinha baixado (rollback medido na change `acesso-do-tutor`).
function "PetBits/registrar_pedido" {
  description = "Baixa estoque, congela precos e grava pedido e itens numa transacao"

  input {
    int id_tutor

    object[] itens {
      schema {
        int produto_id
        int quantidade
      }
    }

    text entrega
    text forma_pagamento
    text situacao
    text endereco?
    text origem
  }

  stack {
    precondition ($input.id_tutor > 0) {
      error_type = "accessdenied"
      error = "Cliente invalido."
    }

    precondition (($input.itens|count) > 0) {
      error_type = "inputerror"
      error = "O pedido precisa de ao menos um item."
    }

    // `pago_em` nasce quando o pedido ja nasce pago (online simulado) ou
    // entregue (balcao).
    var $pago_em {
      value = null
    }

    conditional {
      if (($input.situacao == "pago") || ($input.situacao == "entregue")) {
        var.update $pago_em {
          value = "now"|to_ms
        }
      }
    }

    db.transaction {
      stack {
        var $total {
          value = 0
        }

        var $linhas {
          value = []
        }

        var $valor_linha {
          value = 0
        }

        foreach ($input.itens) {
          each as $item {
            precondition ($item.quantidade > 0) {
              error_type = "inputerror"
              error = "A quantidade de cada item tem de ser pelo menos 1."
            }

            db.query produto {
              where = $db.produto.id == $item.produto_id
              lock = true
              output = ["id", "nome", "preco", "estoque", "ativo"]
              return = {type: "single"}
            } as $produto

            precondition ($produto != null) {
              error_type = "inputerror"
              error = "Um dos produtos nao existe mais."
            }

            precondition ($produto.ativo == true) {
              error_type = "inputerror"
              error = "Um dos produtos nao esta mais a venda: " ~ $produto.nome
            }

            precondition (($produto.estoque > $item.quantidade) || ($produto.estoque == $item.quantidade)) {
              error_type = "inputerror"
              error = "Estoque insuficiente: " ~ $produto.nome
            }

            db.patch produto {
              field_name = "id"
              field_value = $produto.id
              data = {estoque: $produto.estoque - $item.quantidade}
            } as $baixado

            var.update $valor_linha {
              value = $produto.preco * $item.quantidade
            }

            var.update $total {
              value = $total + $valor_linha
            }

            array.push $linhas {
              value = {
                id_produto    : $produto.id
                produto_nome  : $produto.nome
                quantidade    : $item.quantidade
                preco_unitario: $produto.preco
                valor_linha   : $valor_linha
              }
            }
          }
        }

        db.add pedido {
          data = {
            created_at      : "now"
            id_tutor        : $input.id_tutor
            situacao        : $input.situacao
            forma_pagamento : $input.forma_pagamento
            entrega         : $input.entrega
            endereco_entrega: $input.endereco
            total           : $total
            pago_em         : $pago_em
            origem          : $input.origem
          }
        } as $pedido

        foreach ($linhas) {
          each as $linha {
            db.add pedido_item {
              data = {
                created_at    : "now"
                id_pedido     : $pedido.id
                id_produto    : $linha.id_produto
                produto_nome  : $linha.produto_nome
                quantidade    : $linha.quantidade
                preco_unitario: $linha.preco_unitario
                valor_linha   : $linha.valor_linha
              }
            } as $gravado
          }
        }
      }
    }
  }

  response = {id: $pedido.id, total: $pedido.total, situacao: $pedido.situacao}
}
