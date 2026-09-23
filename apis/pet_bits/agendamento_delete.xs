query "agendamento/{id}" verb=DELETE {
  api_group = "PetBits"
  description = "Remove um registro de agendamento"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "agendamento" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
