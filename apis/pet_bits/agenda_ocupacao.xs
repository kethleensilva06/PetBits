// Quem pode atender um servico num dia, e quando cada um ja esta ocupado.
//
// A tela calcula os horarios livres a partir disto (design.md da change
// `agendamento`, D2); quem DECIDE continua sendo o `POST agendamentos`, que
// refaz a conta inteira.
//
// O tutor recebe ids de profissional e intervalos -- sem nome, sem contato,
// sem animal, sem tutor. E o minimo para oferecer horario livre.
query "agenda/ocupacao" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Profissionais compativeis e intervalos ocupados de um dia, para um servico"

  input {
    int servico_id filters=min:1

    // Inicio do dia (meia-noite em Sao Paulo), em ms UTC. A janela e de 24 h
    // a partir dele.
    timestamp dia
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.get servico {
      field_name = "id"
      field_value = $input.servico_id
      output = ["id", "categoria"]
    } as $servico

    precondition ($servico != null) {
      error_type = "inputerror"
      error = "Servico nao encontrado."
    }

    precondition (($servico.categoria == "clinica") || ($servico.categoria == "banho_tosa")) {
      error_type = "inputerror"
      error = "Este servico nao esta disponivel para agendamento."
    }

    // Mesma regra de funcao do POST (D5). Duplicada de proposito em vez de
    // extraida: sao duas linhas, e o POST e o unico que precisa acertar.
    var $funcao_a {
      value = "tosador"
    }

    var $funcao_b {
      value = "tosador"
    }

    conditional {
      if ($servico.categoria == "clinica") {
        var.update $funcao_a {
          value = "veterinario"
        }

        var.update $funcao_b {
          value = "clinico_geral"
        }
      }
    }

    db.query colaborador {
      where = ($db.colaborador.ativo == true) && (($db.colaborador.funcao == $funcao_a) || ($db.colaborador.funcao == $funcao_b))
      sort = {id: "asc"}
      output = ["id"]
      return = {type: "list"}
    } as $profissionais

    var $fim_do_dia {
      value = $input.dia + 86400000
    }

    // Ocupacoes do dia dos profissionais compativeis. O join ate colaborador
    // so serve para filtrar pela funcao; nada dele sai na resposta.
    db.query agendamento {
      join = {
        colaborador: {type: "inner", table: "colaborador", where: $db.agendamento.id_colaborador == $db.colaborador.id}
      }

      where = ($db.agendamento.situacao != "cancelado") && ($fim_do_dia > $db.agendamento.inicio) && ($db.agendamento.fim > $input.dia) && (($db.colaborador.funcao == $funcao_a) || ($db.colaborador.funcao == $funcao_b))
      sort = {inicio: "asc"}
      output = ["id_colaborador", "inicio", "fim"]
      return = {type: "list"}
    } as $ocupados
  }

  response = {profissionais: $profissionais, ocupados: $ocupados}
}
