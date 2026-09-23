table itens_pedido {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Pedido ao qual o item pertence
    int id_pedido {
      table = ""
    }
  
    // Produto vendido
    int id_produto {
      table = ""
    }
  
    // Quantidade vendida
    int quantidade filters=min:0
  
    // Preco unitario no momento da venda
    decimal valor_unitario filters=min:0
  
    // Quantidade multiplicada pelo valor unitario
    decimal valor_total filters=min:0
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pedido", op: "asc"}]}
    {type: "btree", field: [{name: "id_produto", op: "asc"}]}
  ]
}