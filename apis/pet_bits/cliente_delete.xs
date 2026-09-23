// Remove um registro de cliente
query "cliente/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del cliente {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}