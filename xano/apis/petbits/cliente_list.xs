query "cliente" verb=GET {
  api_group = "petbits"
  description = "Lista todos os registros de cliente"
  input {
  }
  stack {
    db.query "cliente" {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
