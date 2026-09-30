// Lista produto. Catalogo: visivel para qualquer pessoa logada.
query produto verb=GET {
  api_group = "PetBits"
  auth = "user"

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
