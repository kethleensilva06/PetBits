// Remove um registro de prontuario
query "prontuario/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del prontuario {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}