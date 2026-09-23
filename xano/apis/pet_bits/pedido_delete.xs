query "pedido/{id}" verb=DELETE {
  api_group = "PetBits"
  description = "Remove um registro de pedido"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "pedido" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
