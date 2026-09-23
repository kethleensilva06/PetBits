// Substitui os campos de um registro de produto; envie o registro completo
query "produto/{id}" verb=PATCH {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  
    // Nome do produto
    text nome? filters=trim
  
    // Categoria do produto
    text categoria? filters=trim
  
    // Marca do produto
    text marca? filters=trim
  
    // Unidade de medida
    text unidade? filters=trim
  
    // Preco de venda
    decimal preco_venda?
  }

  stack {
    db.edit produto {
      field_name = "id"
      field_value = $input.id
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