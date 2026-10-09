// Muda a situacao de um pedido (change `pedidos-da-equipe`).
//
// So pelos caminhos da spec (D2), cada um escrito por IGUALDADE -- a mesma
// regra que a change `operacao-da-clinica` fixou para papel: nunca "qualquer
// coisa diferente de". Transicao fora da tabela: recusa, nada e gravado.
//
// O pedido e lido com TRAVA numa transacao. Cancelar devolve o estoque de
// cada item na MESMA transacao (D4): ou tudo volta, ou nada muda.
query "equipe/pedidos/{pedido_id}/situacao" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Avanca ou cancela um pedido da loja"

  input {
    int pedido_id filters=min:1
    text situacao filters=trim
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

    db.transaction {
      stack {
        db.query pedido {
          where = $db.pedido.id == $input.pedido_id
          lock = true
          output = ["id", "situacao", "entrega", "pago_em"]
          return = {type: "single"}
        } as $pedido

        precondition ($pedido != null) {
          error_type = "notfound"
          error = "Pedido nao encontrado."
        }

        var $permitido {
          value = false
        }

        var $nova {
          value = $input.situacao
        }

        // pendente -> pago | cancelado | pronto_retirada (retirada) | enviado (endereco)
        // pago     -> cancelado | pronto_retirada (retirada) | enviado (endereco)
        conditional {
          if (($pedido.situacao == "pendente") || ($pedido.situacao == "pago")) {
            conditional {
              if ($nova == "cancelado") {
                var.update $permitido {
                  value = true
                }
              }
            }

            conditional {
              if (($nova == "pago") && ($pedido.situacao == "pendente")) {
                var.update $permitido {
                  value = true
                }
              }
            }

            conditional {
              if (($nova == "pronto_retirada") && ($pedido.entrega == "retirada")) {
                var.update $permitido {
                  value = true
                }
              }
            }

            conditional {
              if (($nova == "enviado") && ($pedido.entrega == "endereco")) {
                var.update $permitido {
                  value = true
                }
              }
            }
          }
        }

        // pronto_retirada -> entregue | cancelado
        conditional {
          if ($pedido.situacao == "pronto_retirada") {
            conditional {
              if (($nova == "entregue") || ($nova == "cancelado")) {
                var.update $permitido {
                  value = true
                }
              }
            }
          }
        }

        // enviado -> entregue
        conditional {
          if (($pedido.situacao == "enviado") && ($nova == "entregue")) {
            var.update $permitido {
              value = true
            }
          }
        }

        precondition ($permitido == true) {
          error_type = "inputerror"
          error = "Esta mudanca de situacao nao e permitida para o pedido."
        }

        // D3: a data do pagamento nasce ao ir para `pago`, ou ao ir para
        // `entregue` sem pagamento registrado. Nunca e sobrescrita.
        var $pago_em {
          value = $pedido.pago_em
        }

        conditional {
          if ((($nova == "pago") || ($nova == "entregue")) && (($pedido.pago_em == null) || ($pedido.pago_em == 0))) {
            var.update $pago_em {
              value = "now"|to_ms
            }
          }
        }

        // D4: cancelar devolve o estoque, item por item, sob trava.
        conditional {
          if ($nova == "cancelado") {
            db.query pedido_item {
              where = $db.pedido_item.id_pedido == $pedido.id
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
          }
        }

        db.patch pedido {
          field_name = "id"
          field_value = $pedido.id
          data = {situacao: $nova, pago_em: $pago_em}
        } as $atualizado
      }
    }
  }

  response = {id: $atualizado.id, situacao: $atualizado.situacao, pago_em: $atualizado.pago_em}
}
