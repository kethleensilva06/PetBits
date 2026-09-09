query "servico/{id}" verb=DELETE {
  api_group = "petbits"
  description = "Remove um registro de servico"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "servico" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
