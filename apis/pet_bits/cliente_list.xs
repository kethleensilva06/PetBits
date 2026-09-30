// Lista cliente. So a equipe da clinica.
query cliente verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    precondition ($ctx.is_admin == true) {
      error_type = "accessdenied"
      error = "Apenas a equipe da clinica pode fazer isso."
    }

    db.query cliente {
      sort = {nome: "asc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}
