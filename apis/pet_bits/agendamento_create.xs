// Cria um agendamento.
// O tutor so marca para pet dele, e o status sai sempre como
// "agendado": deixar o corpo da requisicao escolher permitiria
// gravar uma consulta ja como concluida.
query agendamento verb=POST {
  api_group = "PetBits"
  auth = "user"

  input {
    dblink {
      table = "agendamento"
    }
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    db.get pet {
      field_name = "id"
      field_value = $input.id_pet
      output = ["id", "id_cliente"]
    } as $pet

    precondition ($pet != null) {
      error_type = "notfound"
      error = "Pet nao encontrado."
    }

    precondition ($ctx.is_admin == true || $pet.id_cliente == $ctx.cliente_id) {
      error_type = "accessdenied"
      error = "Este pet nao esta na sua conta."
    }

    var $situacao {
      value = $input.status
    }

    conditional {
      if ($ctx.is_admin == false) {
        var.update $situacao {
          value = "agendado"
        }
      }
    }

    db.add agendamento {
      enforce_hidden_fields = false
      data = {created_at: "now", status: $situacao}
    } as $registro
  }

  response = $registro
}
