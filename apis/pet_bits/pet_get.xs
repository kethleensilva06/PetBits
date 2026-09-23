// Busca um registro de pet pelo id
query "pet/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get pet {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}