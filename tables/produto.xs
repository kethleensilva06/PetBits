table produto {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Nome do produto
    text nome filters=trim
  
    // Categoria do produto
    text categoria? filters=trim
  
    // Marca do produto
    text marca? filters=trim
  
    // Unidade de medida
    text unidade? filters=trim
  
    // Preco de venda
    decimal preco_venda filters=min:0
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}