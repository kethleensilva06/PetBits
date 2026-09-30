// Busca um prontuario pelo id.
// O dono e lido do banco, nunca do $input: confiar no corpo da requisicao
// seria deixar qualquer pessoa declarar-se dona do registro.
query "prontuario/{id}" verb=GET {
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

    db.get prontuario {
      field_name = "id"
      field_value = $input.id
    } as $registro

    precondition ($registro != null) {
      error_type = "notfound"
      error = "Registro nao encontrado."
    }

    db.get pet {
      field_name = "id"
      field_value = $registro.id_pet
      output = ["id", "id_cliente"]
    } as $dono

    precondition ($ctx.is_admin == true || $dono.id_cliente == $ctx.cliente_id) {
      error_type = "accessdenied"
      error = "Este registro nao esta na sua conta."
    }
  }

  response = $registro
}
