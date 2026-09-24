// Cria um registro em servico
query servico verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "servico"
    }
  }

  stack {
    db.add servico {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $registro
  }

  response = $registro
}