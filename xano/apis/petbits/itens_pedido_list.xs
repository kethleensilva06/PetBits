query "itens_pedido" verb=GET {
  api_group = "petbits"
  description = "Lista todos os registros de itens_pedido"
  input {
  }
  stack {
    db.query "itens_pedido" {
      sort = {id: "asc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
