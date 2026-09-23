query "produto/{id}" verb=GET {
  api_group = "PetBits"
  description = "Busca um registro de produto pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "produto" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
