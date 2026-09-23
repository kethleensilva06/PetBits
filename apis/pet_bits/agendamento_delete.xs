// Remove um registro de agendamento
query "agendamento/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del agendamento {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}