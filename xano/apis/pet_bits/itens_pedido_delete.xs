query "itens_pedido/{id}" verb=DELETE {
  api_group = "PetBits"
  description = "Remove um registro de itens_pedido"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.del "itens_pedido" {
      field_name = "id"
      field_value = $input.id
    }
  }
  response = {success: true}
}
