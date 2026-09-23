// Remove um registro de funcionario
query "funcionario/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del funcionario {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}