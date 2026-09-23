// Cria um registro em produto
query produto verb=POST {
  api_group = "PetBits"

  input {
    // Nome do produto
    text nome filters=trim
  
    // Categoria do produto
    text categoria? filters=trim
  
    // Marca do produto
    text marca? filters=trim
  
    // Unidade de medida
    text unidade? filters=trim
  
    // Preco de venda
    decimal preco_venda
  }

  stack {
    db.add produto {
      data = {
        nome       : $input.nome
        categoria  : $input.categoria
        marca      : $input.marca
        unidade    : $input.unidade
        preco_venda: $input.preco_venda
      }
    } as $registro
  }

  response = $registro
}