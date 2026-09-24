// Cria um registro em produto
query produto verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "produto"
    }
  }

  stack {
    db.add produto {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $registro
  }

  response = $registro
}