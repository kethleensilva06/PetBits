// Busca um registro de pedido pelo id
query "pedido/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get pedido {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}