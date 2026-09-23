// Busca um registro de produto pelo id
query "produto/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get produto {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}