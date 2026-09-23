// Cria um registro em itens_pedido
query itens_pedido verb=POST {
  api_group = "PetBits"

  input {
    // Pedido ao qual o item pertence
    int id_pedido
  
    // Produto vendido
    int id_produto
  
    // Quantidade vendida
    int quantidade
  
    // Preco unitario no momento da venda
    decimal valor_unitario
  
    // Quantidade multiplicada pelo valor unitario
    decimal valor_total
  }

  stack {
    db.add itens_pedido {
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