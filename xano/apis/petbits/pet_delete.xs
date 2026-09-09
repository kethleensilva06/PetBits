query "pet/{id}" verb=DELETE {
  api_group = "petbits"
  description = "Remove um registro de pet"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "pet" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
