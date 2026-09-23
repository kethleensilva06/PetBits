// Lista todos os registros de pedido
query pedido verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query pedido {
      sort = {data_pedido: "desc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}