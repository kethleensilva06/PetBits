// Registra um atendimento -- ou uma retificacao (change `historico-clinico`,
// D2 e D4).
//
// O UNICO endpoint de escrita do historico, e so cria. Nao existe PATCH nem
// DELETE de atendimento: a garantia de que o historico nao se apaga e
// estrutural, nao uma regra que alguem possa esquecer.
//
// Tudo e conferido antes de gravar: prova de equipe; animal existe; quem
// atendeu esta ativo e e veterinario ou clinico geral; diagnostico nao vazio;
// data nao futura; retorno nao antes da data; retificacao do MESMO animal;
// agendamento do mesmo animal, nem cancelado nem concluido. Com agendamento,
// o registro e a conclusao dele vao na mesma transacao.
query "equipe/atendimentos" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Registra um atendimento (ou retificacao) no historico de um animal"

  input {
    int pet_id filters=min:1
    int id_colaborador filters=min:1
    timestamp data_atendimento?
    text motivo? filters=trim
    text diagnostico filters=trim
    text tratamento? filters=trim
    decimal peso?
    timestamp retorno?
    int id_agendamento?
    int retifica?
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

    precondition ($input.diagnostico != "") {
      error_type = "inputerror"
      error = "O diagnostico nao pode ficar em branco."
    }

    db.query pet {
      where = $db.pet.id == $input.pet_id
      output = ["id"]
      return = {type: "single"}
    } as $animal

    precondition ($animal != null) {
      error_type = "notfound"
      error = "Animal nao encontrado."
    }

    db.query colaborador {
      where = $db.colaborador.id == $input.id_colaborador
      output = ["id", "funcao", "ativo"]
      return = {type: "single"}
    } as $quem

    precondition ($quem != null) {
      error_type = "notfound"
      error = "Colaborador nao encontrado."
    }

    precondition ($quem.ativo != false) {
      error_type = "inputerror"
      error = "Este colaborador esta desligado da clinica."
    }

    precondition (($quem.funcao == "veterinario") || ($quem.funcao == "clinico_geral")) {
      error_type = "inputerror"
      error = "O atendimento precisa ser de um veterinario ou clinico geral."
    }

    var $agora {
      value = "now"|to_ms
    }

    var $data {
      value = $input.data_atendimento
    }

    conditional {
      if (($data == null) || ($data == 0)) {
        var.update $data {
          value = $agora
        }
      }
    }

    precondition ($data <= $agora) {
      error_type = "inputerror"
      error = "A data do atendimento nao pode ser no futuro."
    }

    conditional {
      if (($input.retorno != null) && ($input.retorno != 0)) {
        precondition ($input.retorno >= $data) {
          error_type = "inputerror"
          error = "O retorno nao pode ser antes do atendimento."
        }
      }
    }

    conditional {
      if ($input.retifica > 0) {
        db.query atendimento {
          where = $db.atendimento.id == $input.retifica
          output = ["id", "id_pet"]
          return = {type: "single"}
        } as $corrigido

        precondition (($corrigido != null) && ($corrigido.id_pet == $animal.id)) {
          error_type = "inputerror"
          error = "A retificacao precisa ser de um atendimento deste animal."
        }
      }
    }

    conditional {
      if ($input.id_agendamento > 0) {
        db.query agendamento {
          where = $db.agendamento.id == $input.id_agendamento
          output = ["id", "id_pet", "situacao"]
          return = {type: "single"}
        } as $marcado

        precondition (($marcado != null) && ($marcado.id_pet == $animal.id)) {
          error_type = "inputerror"
          error = "Este agendamento nao e deste animal."
        }

        precondition (($marcado.situacao != "cancelado") && ($marcado.situacao != "concluido")) {
          error_type = "inputerror"
          error = "Este agendamento ja foi cancelado ou concluido."
        }
      }
    }

    db.transaction {
      stack {
        db.add atendimento {
          data = {
            created_at      : "now"
            id_pet          : $animal.id
            id_colaborador  : $quem.id
            id_agendamento  : $input.id_agendamento
            retifica        : $input.retifica
            data_atendimento: $data
            motivo          : $input.motivo
            diagnostico     : $input.diagnostico
            tratamento      : $input.tratamento
            peso            : $input.peso
            retorno         : $input.retorno
            registrado_por  : $id_conta
          }
        } as $novo

        conditional {
          if ($input.id_agendamento > 0) {
            db.patch agendamento {
              field_name = "id"
              field_value = $input.id_agendamento
              data = {situacao: "concluido"}
            } as $concluido
          }
        }
      }
    }
  }

  response = {
    id              : $novo.id
    id_pet          : $novo.id_pet
    data_atendimento: $novo.data_atendimento
    diagnostico     : $novo.diagnostico
    retifica        : $novo.retifica
  }
}
