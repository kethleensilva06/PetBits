query "pedido/{id}" verb=GET {
  api_group = "petbits"
  description = "Busca um registro de pedido pelo id"
  input {
    int id {
      description = "Identificador do registro"
    }
  }
  stack {
    db.get "pedido" {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }
  response = $registro
}
