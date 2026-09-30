// Atualiza um pet.
// Para o tutor, id_cliente e id saem do corpo antes de gravar. O
// filter_null nao serve para isso: ele descarta nulo, nao um inteiro
// forjado -- e reapontar id_cliente entregaria o pet a outra conta.
query "pet/{pet_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"

  input {
    int pet_id? filters=min:1
    dblink {
      table = "pet"
    }
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    db.get pet {
      field_name = "id"
      field_value = $input.pet_id
    } as $atual

    precondition ($atual != null) {
      error_type = "notfound"
      error = "Pet nao encontrado."
    }

    precondition ($ctx.is_admin == true || $atual.id_cliente == $ctx.cliente_id) {
      error_type = "accessdenied"
      error = "Este pet nao esta na sua conta."
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
        var.update $dados {
          value = $dados|unset:"id_cliente"|unset:"id"
        }
      }
    }

    db.patch pet {
      field_name = "id"
      field_value = $input.pet_id
      data = $dados
    } as $registro
  }

  response = $registro
}
