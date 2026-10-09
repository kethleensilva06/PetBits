// Uma compra de um tutor na loja (change `loja`, D1).
//
// O tutor vem SEMPRE do token (`tutor_do_token`), nunca da requisicao. O
// total e DERIVADO dos itens e calculado no servidor (modelo de dominio) --
// esta coluna so guarda o resultado, para a lista nao precisar somar.
table pedido {
  auth = false

  schema {
    int id

    int id_tutor {
      table = "tutor"
    }

    // `pronto_retirada`, `enviado` e `entregue` sao da change
    // `pedidos-da-equipe`; esta so cria `pendente` e `pago`.
    enum situacao?=pendente {
      values = ["pendente", "pago", "pronto_retirada", "enviado", "entregue", "cancelado"]
    }

    // `online` e SIMULADO (D3): nada e cobrado, nenhum dado de pagamento e
    // guardado.
    enum forma_pagamento {
      values = ["na_loja", "online"]
    }

    enum entrega {
      values = ["retirada", "endereco"]
    }

    // Copiado da ficha do tutor na hora da compra (D4).
    text endereco_entrega? filters=trim

    decimal total

    timestamp pago_em?
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_tutor", op: "asc"}, {name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "situacao", op: "asc"}]}
  ]
}
