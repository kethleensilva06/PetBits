// Busca um cliente pelo id. So a equipe da clinica.
query "cliente/{id}" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
    // Identificador do registro
    int id
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    precondition ($ctx.is_admin == true) {
      error_type = "accessdenied"
      error = "Apenas a equipe da clinica pode fazer isso."
    }

    db.get cliente {
      field_name = "id"
      field_value = $input.id
    } as $registro
  }

  response = $registro
}
