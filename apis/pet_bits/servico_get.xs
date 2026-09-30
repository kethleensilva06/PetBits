// Busca um servico pelo id. Catalogo: qualquer pessoa logada ve.
query "servico/{id}" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get servico {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}
