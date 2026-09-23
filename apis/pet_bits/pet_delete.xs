// Remove um registro de pet
query "pet/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del pet {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}