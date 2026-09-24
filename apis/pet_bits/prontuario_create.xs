// Cria um registro em prontuario
query prontuario verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "prontuario"
    }
  }

  stack {
    db.add prontuario {
      enforce_hidden_fields = false
      data = {created_at: "now", data_atendimento: "now"}
    } as $registro
  }

  response = $registro
}
