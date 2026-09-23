// Lista todos os registros de pet
query pet verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query pet {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}