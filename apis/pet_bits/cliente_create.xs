// Cria um registro em cliente
query cliente verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "cliente"
    }
  }

  stack {
    db.add cliente {
      enforce_hidden_fields = false
      data = {created_at: "now", data_cadastro: "now"}
    } as $registro
  }

  response = $registro
}