// Lista todos os registros de cliente
query cliente verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query cliente {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}