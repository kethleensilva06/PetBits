// Substitui os campos de um registro de pedido; envie o registro completo
query "pedido/{id}" verb=PATCH {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  
    // Cliente do pedido
    int id_cliente?
  
    // pendente, pago, enviado ou entregue
    text status? filters=trim
  
    // Soma dos itens do pedido
    decimal valor_total?
  }

  stack {
    db.edit pedido {
      field_name = "id"
      field_value = $input.id
      data = {
        id_cliente : $input.id_cliente
        status     : $input.status
        valor_total: $input.valor_total
      }
    } as $registro
  }

  response = $registro
}