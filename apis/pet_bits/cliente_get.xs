// Busca um registro de cliente pelo id
query "cliente/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get cliente {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}