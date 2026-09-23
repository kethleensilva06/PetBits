// Busca um registro de agendamento pelo id
query "agendamento/{id}" verb=GET {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get agendamento {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}