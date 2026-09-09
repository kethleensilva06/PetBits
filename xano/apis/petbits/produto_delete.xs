query "produto/{id}" verb=DELETE {
  api_group = "petbits"
  description = "Remove um registro de produto"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "produto" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
