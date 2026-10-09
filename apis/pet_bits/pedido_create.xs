// Faz um pedido na loja para o tutor autenticado (change `loja`).
//
// Do cliente vem so produto e quantidade de cada item, a entrega e a forma de
// pagamento. O DONO vem do token (`tutor_do_token`); o PRECO vem do
// catalogo, congelado no item; a linha e o total sao calculados aqui. Um
// `preco` ou `total` mandado no corpo nao existe no `input` e e ignorado.
//
// Tudo numa transacao (D2): para cada item, o produto e lido com TRAVA, o
// estoque e conferido e baixado, e so no fim o pedido e os itens sao
// gravados. Qualquer recusa no meio desfaz o que ja tinha baixado. A trava
// serializa dois pedidos da mesma unidade: o segundo le o estoque ja baixado.
query pedidos verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Faz um pedido na loja para o tutor autenticado"

  input {
    object[] itens {
      schema {
        int produto_id
        int quantidade
      }
    }

    text entrega filters=trim
    text forma_pagamento filters=trim
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/tutor_do_token" {
      input = {user_id: $auth.id}
    } as $id_tutor

    precondition ($id_tutor > 0) {
      error_type = "accessdenied"
      error = "Esta conta nao tem cadastro de cliente."
    }

    precondition (($input.itens|count) > 0) {
      error_type = "inputerror"
      error = "O pedido precisa de ao menos um item."
    }

    precondition (($input.entrega == "retirada") || ($input.entrega == "endereco")) {
      error_type = "inputerror"
      error = "Forma de entrega invalida."
    }

    precondition (($input.forma_pagamento == "na_loja") || ($input.forma_pagamento == "online")) {
      error_type = "inputerror"
      error = "Forma de pagamento invalida."
    }

    // D4: endereco congelado da ficha, so quando a entrega e no endereco.
    var $endereco {
      value = ""
    }

    conditional {
      if ($input.entrega == "endereco") {
        db.get tutor {
          field_name = "id"
          field_value = $id_tutor
          output = ["endereco"]
        } as $ficha

        var.update $endereco {
          value = $ficha.endereco
        }

        precondition (($endereco != null) && ($endereco != "")) {
          error_type = "inputerror"
          error = "Seu cadastro nao tem endereco. Escolha retirada na clinica."
        }
      }
    }

    // D3: online e SIMULADO -- nasce pago, nada e cobrado.
    var $situacao {
      value = "pendente"
    }

    var $pago_em {
      value = null
    }

    conditional {
      if ($input.forma_pagamento == "online") {
        var.update $situacao {
          value = "pago"
        }

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
            id_tutor        : $id_tutor
            situacao        : $situacao
            forma_pagamento : $input.forma_pagamento
            entrega         : $input.entrega
            endereco_entrega: $endereco
            total           : $total
            pago_em         : $pago_em
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
