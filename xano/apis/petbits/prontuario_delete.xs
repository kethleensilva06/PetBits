query "prontuario/{id}" verb=DELETE {
  api_group = "petbits"
  description = "Remove um registro de prontuario"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "prontuario" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
