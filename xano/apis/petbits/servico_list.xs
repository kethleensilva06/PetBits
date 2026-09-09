query "servico" verb=GET {
  api_group = "petbits"
  description = "Lista todos os registros de servico"
  input {
  }
  stack {
    db.query "servico" {
      sort = {nome_servico: "asc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
