// Cria um itens_pedido. So a equipe da clinica.
query itens_pedido verb=POST {
  api_group = "PetBits"
  auth = "user"

  input {
    dblink {
      table = "itens_pedido"
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

    db.add itens_pedido {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $registro
  }

  response = $registro
}
