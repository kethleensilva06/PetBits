// Cria um pedido. So a equipe da clinica.
query pedido verb=POST {
  api_group = "PetBits"
  auth = "user"

  input {
    dblink {
      table = "pedido"
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

    db.add pedido {
      enforce_hidden_fields = false
      data = {created_at: "now", data_pedido: "now"}
    } as $registro
  }

  response = $registro
}
