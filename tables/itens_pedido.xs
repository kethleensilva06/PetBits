table "itens_pedido" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

    int id_pedido {
      table = "pedido"
      description = "Pedido ao qual o item pertence"
    }

    int id_produto {
      table = "produto"
      description = "Produto vendido"
    }

    int quantidade filters=min:0 {
      description = "Quantidade vendida"
    }

    decimal valor_unitario filters=min:0 {
      description = "Preco unitario no momento da venda"
    }

    decimal valor_total filters=min:0 {
      description = "Quantidade multiplicada pelo valor unitario"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pedido", op: "asc"}]}
    {type: "btree", field: [{name: "id_produto", op: "asc"}]}
  ]
}
