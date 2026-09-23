// Lista todos os registros de servico
query servico verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query servico {
      sort = {nome_servico: "asc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}