// Lista todos os registros de funcionario
query funcionario verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query funcionario {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}