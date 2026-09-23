// Remove um registro de itens_pedido
query "itens_pedido/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del itens_pedido {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}