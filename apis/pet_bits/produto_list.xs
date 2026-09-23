// Lista todos os registros de produto
query produto verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query produto {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}