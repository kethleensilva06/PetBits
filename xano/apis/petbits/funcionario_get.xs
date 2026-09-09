query "funcionario/{id}" verb=GET {
  api_group = "petbits"
  description = "Busca um registro de funcionario pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "funcionario" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
