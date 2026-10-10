// Venda no balcao, registrada pela equipe na conta de um cliente (change
// `venda-no-balcao`).
//
// Diferente do site, o cliente vem do CORPO -- quem pede e a equipe (D3). E
// seguro porque este e um `equipe_*`, com a prova antes de tudo (conferida
// pela guarda `verificar_equipe.py`), e o cliente e lido do banco: id
// inexistente e recusado. A venda nasce entregue e paga (D2), e a regra de
// estoque e a mesma do site, pela funcao `PetBits/registrar_pedido` (D1).
query "equipe/vendas" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Registra uma venda presencial na conta de um cliente"

  input {
    int tutor_id filters=min:1

    object[] itens {
      schema {
        int produto_id
        int quantidade
      }
    }
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

    db.get tutor {
      field_name = "id"
      field_value = $input.tutor_id
      output = ["id"]
    } as $cliente

    precondition ($cliente != null) {
      error_type = "inputerror"
      error = "Cliente nao encontrado."
    }

    function.run "PetBits/registrar_pedido" {
      input = {
        id_tutor       : $cliente.id
        itens          : $input.itens
        entrega        : "retirada"
        forma_pagamento: "na_loja"
        situacao       : "entregue"
        endereco       : ""
        origem         : "balcao"
      }
    } as $venda
  }

  response = $venda
}
