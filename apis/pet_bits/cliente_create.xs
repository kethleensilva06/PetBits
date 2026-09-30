// Cria um cliente. So a equipe da clinica.
query cliente verb=POST {
  api_group = "PetBits"
  auth = "user"

  input {
    dblink {
      table = "cliente"
      override = {
        id_user: {hidden: true}
      }
    }
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    precondition ($ctx.is_admin == true) {
      error_type = "accessdenied"
      error = "Apenas a equipe da clinica pode fazer isso."
    }

    db.add cliente {
      enforce_hidden_fields = false
      data = {created_at: "now", data_cadastro: "now"}
    } as $registro
  }

  response = $registro
}
