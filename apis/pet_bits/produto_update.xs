// Atualiza um produto. So a equipe da clinica.
query "produto/{produto_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"

  input {
    int produto_id? filters=min:1
    dblink {
      table = "produto"
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

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.patch produto {
      field_name = "id"
      field_value = $input.produto_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}
