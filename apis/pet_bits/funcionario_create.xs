// Cria um registro em funcionario
query funcionario verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "funcionario"
    }
  }

  stack {
    db.add funcionario {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $registro
  }

  response = $registro
}
