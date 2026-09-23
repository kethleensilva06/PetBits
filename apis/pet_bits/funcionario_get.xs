// Busca um registro de funcionario pelo id
query "funcionario/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get funcionario {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}