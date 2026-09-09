query "cliente/{id}" verb=DELETE {
  api_group = "petbits"
  description = "Remove um registro de cliente"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "cliente" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
