// Cancela um agendamento de um animal do tutor autenticado, ate 24 h antes.
//
// Posse pelo join (design.md da change `agendamento`, D6): agendamento alheio
// e agendamento inexistente respondem igual, "nao encontrado". O prazo e
// medido pelo relogio do Xano, nunca por um horario mandado pelo cliente.
//
// Cancelar NAO apaga (modelo de dominio): muda a situacao e registra quando.
// O intervalo volta a ficar livre porque toda conferencia de sobreposicao
// ignora `cancelado`.
query "agendamentos/{agendamento_id}/cancelar" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cancela um agendamento do tutor autenticado, ate 24 horas antes"

  input {
    int agendamento_id filters=min:1
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.transaction {
      stack {
        db.query agendamento {
          join = {
            pet  : {type: "inner", table: "pet", where: $db.agendamento.id_pet == $db.pet.id}
            tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
          }

          where = ($db.agendamento.id == $input.agendamento_id) && ($db.tutor.id_user == $auth.id)
          lock = true
          output = ["id", "inicio", "situacao"]
          return = {type: "single"}
        } as $meu

        precondition ($meu != null) {
          error_type = "notfound"
          error = "Agendamento nao encontrado."
        }

        precondition ($meu.situacao == "marcado") {
          error_type = "inputerror"
          error = "Este agendamento nao pode mais ser cancelado."
        }

        precondition ((($meu.inicio - ("now"|to_ms)) > 86400000) || (($meu.inicio - ("now"|to_ms)) == 86400000)) {
          error_type = "inputerror"
          error = "Faltam menos de 24 horas. Para cancelar, fale com a clinica."
        }

        db.patch agendamento {
          field_name = "id"
          field_value = $meu.id
          data = {situacao: "cancelado", cancelado_em: "now"}
        } as $cancelado
      }
    }
  }

  response = {id: $cancelado.id, situacao: $cancelado.situacao, cancelado_em: $cancelado.cancelado_em}
}
