query "funcionario" verb=GET {
  api_group = "petbits"
  description = "Lista todos os registros de funcionario"
  input {
  }
  stack {
    db.query "funcionario" {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
