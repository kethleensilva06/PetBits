// Busca um registro de prontuario pelo id
query "prontuario/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get prontuario {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}