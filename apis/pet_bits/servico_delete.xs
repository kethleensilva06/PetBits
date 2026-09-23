// Remove um registro de servico
query "servico/{id}" verb=DELETE {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.del servico {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}