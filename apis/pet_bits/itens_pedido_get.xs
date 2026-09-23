query "itens_pedido/{id}" verb=GET {
  api_group = "PetBits"
  description = "Busca um registro de itens_pedido pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "itens_pedido" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
