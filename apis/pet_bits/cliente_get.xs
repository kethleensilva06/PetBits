query "cliente/{id}" verb=GET {
  api_group = "PetBits"
  description = "Busca um registro de cliente pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "cliente" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
