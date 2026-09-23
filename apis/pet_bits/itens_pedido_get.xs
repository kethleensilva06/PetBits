// Busca um registro de itens_pedido pelo id
query "itens_pedido/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get itens_pedido {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}