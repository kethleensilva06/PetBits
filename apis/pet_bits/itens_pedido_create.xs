// Cria um registro em itens_pedido
query itens_pedido verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "itens_pedido"
    }
  }

  stack {
    db.add itens_pedido {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $registro
  }

  response = $registro
}