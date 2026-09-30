// Lista servico. Catalogo: visivel para qualquer pessoa logada.
query servico verb=GET {
  api_group = "PetBits"
  auth = "user"

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
