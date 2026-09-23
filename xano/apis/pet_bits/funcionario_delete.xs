query "funcionario/{id}" verb=DELETE {
  api_group = "PetBits"
  description = "Remove um registro de funcionario"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "funcionario" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
