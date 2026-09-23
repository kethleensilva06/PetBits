// Cria um registro em pedido
query pedido verb=POST {
  api_group = "PetBits"

  input {
    // Cliente do pedido
    int id_cliente
  
    // pendente, pago, enviado ou entregue
    text status filters=trim
  
    // Soma dos itens do pedido
    decimal valor_total?
  }

  stack {
    db.add pedido {
      data = {
        id_cliente : $input.id_cliente
        status     : $input.status
        valor_total: $input.valor_total
      }
    } as $registro
  }

  response = $registro
}