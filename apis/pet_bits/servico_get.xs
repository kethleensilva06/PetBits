// Busca um registro de servico pelo id
query "servico/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get servico {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}