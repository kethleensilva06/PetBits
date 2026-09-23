// Remove um registro de produto
query "produto/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del produto {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}