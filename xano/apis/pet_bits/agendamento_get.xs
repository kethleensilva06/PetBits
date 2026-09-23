query "agendamento/{id}" verb=GET {
  api_group = "PetBits"
  description = "Busca um registro de agendamento pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "agendamento" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
