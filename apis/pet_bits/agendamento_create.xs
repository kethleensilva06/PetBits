// Cria um registro em agendamento
query agendamento verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "agendamento"
    }
  }

  stack {
    db.add agendamento {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $registro
  }

  response = $registro
}
