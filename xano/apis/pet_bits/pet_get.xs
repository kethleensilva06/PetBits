query "pet/{id}" verb=GET {
  api_group = "PetBits"
  description = "Busca um registro de pet pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "pet" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
