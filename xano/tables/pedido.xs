table "pedido" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

    int id_cliente {
      table = "cliente"
      description = "Cliente do pedido"
    }

    text status filters=trim {
      description = "pendente, pago, enviado ou entregue"
    }

    decimal valor_total? filters=min:0 {
      description = "Soma dos itens do pedido"
    }

    timestamp data_pedido?=now {
      description = "Momento do pedido"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_cliente", op: "asc"}]}
    {type: "btree", field: [{name: "data_pedido", op: "desc"}]}
  ]
}
