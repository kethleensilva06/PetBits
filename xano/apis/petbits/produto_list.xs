query "produto" verb=GET {
  api_group = "petbits"
  description = "Lista todos os registros de produto"
  input {
  }
  stack {
    db.query "produto" {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
