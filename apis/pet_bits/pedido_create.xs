// Cria um registro em pedido
query pedido verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "pedido"
    }
  }

  stack {
    db.add pedido {
      enforce_hidden_fields = false
      data = {created_at: "now", data_pedido: "now"}
    } as $registro
  }

  response = $registro
}