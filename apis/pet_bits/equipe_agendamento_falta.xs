// A equipe registra que o animal nao compareceu (change `nao-compareceu`).
//
// Mesma abertura de todo `equipe_*`, conferida pela guarda
// `scripts/verificar_equipe.py`. So `marcado` (D2), e so depois que o horario
// comecou, pelo relogio do Xano: antes disso e engano, e o horario ainda pode
// ser usado. Lido com trava numa transacao, e escrito por igualdade.
//
// Nao desfaz (D3): `faltou` nao volta a `marcado` por aqui.
query "equipe/agendamentos/{agendamento_id}/falta" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Registra que o animal nao compareceu a um agendamento que ja comecou"

  input {
    int agendamento_id filters=min:1
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    db.transaction {
      stack {
        db.query agendamento {
          where = $db.agendamento.id == $input.agendamento_id
          lock = true
          output = ["id", "inicio", "situacao"]
          return = {type: "single"}
        } as $agendamento

        precondition ($agendamento != null) {
          error_type = "notfound"
          error = "Agendamento nao encontrado."
        }

        precondition ($agendamento.situacao == "marcado") {
          error_type = "inputerror"
          error = "So um agendamento marcado pode ter falta registrada."
        }

        precondition ((("now"|to_ms) > $agendamento.inicio) || (("now"|to_ms) == $agendamento.inicio)) {
          error_type = "inputerror"
          error = "O horario deste agendamento ainda nao chegou."
        }

        db.patch agendamento {
          field_name = "id"
          field_value = $agendamento.id
          data = {situacao: "faltou"}
        } as $faltou
      }
    }
  }

  response = {id: $faltou.id, situacao: $faltou.situacao}
}
