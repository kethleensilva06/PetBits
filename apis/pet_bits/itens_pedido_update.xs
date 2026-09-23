// Substitui os campos de um registro de itens_pedido; envie o registro completo
query "itens_pedido/{id}" verb=PATCH {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  
    // Pedido ao qual o item pertence
    int id_pedido?
  
    // Produto vendido
    int id_produto?
  
    // Quantidade vendida
    int quantidade?
  
    // Preco unitario no momento da venda
    decimal valor_unitario?
  
    // Quantidade multiplicada pelo valor unitario
    decimal valor_total?
  }

  stack {
    db.edit itens_pedido {
      field_name = "id"
      field_value = $input.id
      data = {
        id_pedido     : $input.id_pedido
        id_produto    : $input.id_produto
        quantidade    : $input.quantidade
        valor_unitario: $input.valor_unitario
        valor_total   : $input.valor_total
      }
    } as $registro
  }

  response = $registro
}