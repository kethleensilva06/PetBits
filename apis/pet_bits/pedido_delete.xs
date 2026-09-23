// Remove um registro de pedido
query "pedido/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del pedido {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}