table pedido {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Cliente do pedido
    int id_cliente {
      table = "cliente"
    }
  
    // pendente, pago, enviado ou entregue
    text status filters=trim
  
    // Soma dos itens do pedido
    decimal valor_total? filters=min:0
  
    // Momento do pedido
    timestamp data_pedido?=now
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_cliente", op: "asc"}]}
    {type: "btree", field: [{name: "data_pedido", op: "desc"}]}
  ]
}