// Remove um pedido. So a equipe da clinica: apagar deixa os registros
// ligados apontando para o vazio, e o tutor tem o cancelamento para o
// que ele precisa desfazer.
query "pedido/{id}" verb=DELETE {
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

    db.del pedido {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}
