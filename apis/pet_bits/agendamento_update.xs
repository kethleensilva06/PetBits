// Atualiza um agendamento.
// A unica alteracao que o tutor pode fazer e cancelar, e o corpo dele
// e descartado inteiro em favor de {status: "cancelado"}: senao ele
// remarcaria por cima de um horario ja ocupado, ou passaria a consulta
// para outro pet.
query "agendamento/{agendamento_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"

  input {
    int agendamento_id? filters=min:1
    dblink {
      table = "agendamento"
    }
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    db.get agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
    } as $atual

    precondition ($atual != null) {
      error_type = "notfound"
      error = "Agendamento nao encontrado."
    }

    db.get pet {
      field_name = "id"
      field_value = $atual.id_pet
      output = ["id", "id_cliente"]
    } as $pet

    precondition ($ctx.is_admin == true || $pet.id_cliente == $ctx.cliente_id) {
      error_type = "accessdenied"
      error = "Esta consulta nao esta na sua conta."
    }

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    var $dados {
      value = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    }

    conditional {
      if ($ctx.is_admin == false) {
        precondition ($input.status == "cancelado") {
          error_type = "accessdenied"
          error = "Voce so pode cancelar uma consulta. Para remarcar, marque uma nova."
        }

        var.update $dados {
          value = {status: "cancelado"}
        }
      }
    }

    db.patch agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
      data = $dados
    } as $registro
  }

  response = $registro
}
