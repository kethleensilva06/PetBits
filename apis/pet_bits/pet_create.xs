// Cria um pet.
// O dblink transforma toda coluna da tabela em entrada, inclusive
// id_cliente. Para o tutor esse valor e ignorado e trocado pela ficha
// dele: sem isso, bastaria mandar outro id para cadastrar um pet na
// conta de outra pessoa.
query pet verb=POST {
  api_group = "PetBits"
  auth = "user"

  input {
    dblink {
      table = "pet"
    }
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    var $dono {
      value = $input.id_cliente
    }

    conditional {
      if ($ctx.is_admin == false) {
        var.update $dono {
          value = $ctx.cliente_id
        }
      }
    }

    db.add pet {
      enforce_hidden_fields = false
      data = {created_at: "now", id_cliente: $dono}
    } as $registro
  }

  response = $registro
}
