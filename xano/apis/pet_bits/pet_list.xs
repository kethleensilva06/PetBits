query "pet" verb=GET {
  api_group = "PetBits"
  description = "Lista todos os registros de pet"
  input {
  }
  stack {
    db.query "pet" {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
