// Lista agendamento.
// O dono de agendamento esta a um salto: o filtro entra como join, para
// o recorte acontecer no banco e nao depois de baixar a tabela toda.
query agendamento verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    var $registros {
      value = []
    }

    conditional {
      if ($ctx.is_admin == true) {
        db.query agendamento {
          sort = {data_hora: "desc"}
          return = {type: "list"}
        } as $todos

        var.update $registros {
          value = $todos
        }
      }
      else {
        db.query agendamento {
          join = {
            pet: {table: "pet", where: $db.agendamento.id_pet == $db.pet.id}
          }

          where = $db.pet.id_cliente == $ctx.cliente_id
          sort = {data_hora: "desc"}
          return = {type: "list"}
        } as $meus

        var.update $registros {
          value = $meus
        }
      }
    }
  }

  response = $registros
}
