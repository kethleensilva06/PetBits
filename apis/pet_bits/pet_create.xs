// Cria um registro em pet
query pet verb=POST {
  api_group = "PetBits"

  input {
    dblink {
      table = "pet"
    }
  }

  stack {
    db.add pet {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $registro
  }

  response = $registro
}
