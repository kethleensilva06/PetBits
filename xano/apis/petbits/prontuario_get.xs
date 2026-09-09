query "prontuario/{id}" verb=GET {
  api_group = "petbits"
  description = "Busca um registro de prontuario pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "prontuario" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
