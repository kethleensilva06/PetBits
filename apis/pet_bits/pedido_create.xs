// Faz um pedido na loja para o tutor autenticado (change `loja`).
//
// Do cliente vem so produto e quantidade de cada item, a entrega e a forma de
// pagamento. O DONO vem do token (`tutor_do_token`). Um `preco` ou `total`
// mandado no corpo nao existe no `input` e e ignorado.
//
// A regra de estoque -- trava por produto, conferencia, baixa, preco
// congelado, total -- mora em `PetBits/registrar_pedido` desde a change
// `venda-no-balcao` (D1), que o balcao tambem usa. Aqui fica o que e do SITE:
// dono pelo token, entrega, endereco da ficha e o pagamento online simulado.
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

    precondition (($input.entrega == "retirada") || ($input.entrega == "endereco")) {
      error_type = "inputerror"
      error = "Forma de entrega invalida."
    }

    precondition (($input.forma_pagamento == "na_loja") || ($input.forma_pagamento == "online")) {
      error_type = "inputerror"
      error = "Forma de pagamento invalida."
    }

    // D4 da change `loja`: endereco congelado da ficha, so quando a entrega e
    // no endereco.
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

    // D3 da change `loja`: online e SIMULADO -- nasce pago, nada e cobrado.
    var $situacao {
      value = "pendente"
    }

    conditional {
      if ($input.forma_pagamento == "online") {
        var.update $situacao {
          value = "pago"
        }
      }
    }

    function.run "PetBits/registrar_pedido" {
      input = {
        id_tutor       : $id_tutor
        itens          : $input.itens
        entrega        : $input.entrega
        forma_pagamento: $input.forma_pagamento
        situacao       : $situacao
        endereco       : $endereco
        origem         : "site"
      }
    } as $pedido
  }

  response = $pedido
}
