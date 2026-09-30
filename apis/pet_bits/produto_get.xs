// Busca um produto pelo id. Catalogo: qualquer pessoa logada ve.
query "produto/{id}" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
    // Identificador do registro
    int id
  }

  stack {
    db.get produto {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}
