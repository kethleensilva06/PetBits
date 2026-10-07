// Marca um agendamento para um animal do tutor autenticado.
//
// E AQUI que as regras da agenda valem (design.md da change `agendamento`,
// D2). A tela so sugere horarios; este endpoint refaz a conta inteira --
// posse, categoria, grade, futuro, expediente, profissional livre -- e so
// entao grava. Uma requisicao forjada passa pelas mesmas recusas.
//
// O profissional NAO e entrada: o sistema escolhe (decisao da clinica).
// Nada que o cliente mande pode virar o colaborador do agendamento.
query agendamentos verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Marca um agendamento para um animal do tutor autenticado"

  input {
    int pet_id filters=min:1
    int servico_id filters=min:1
    timestamp inicio
    text observacoes? filters=trim
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    // Posse pelo join, no padrao de `pet_get`: animal alheio e animal
    // inexistente recusam igual.
    db.query pet {
      join = {
        tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
      }

      where = ($db.pet.id == $input.pet_id) && ($db.tutor.id_user == $auth.id)
      output = ["id"]
      return = {type: "single"}
    } as $animal

    precondition ($animal != null) {
      error_type = "inputerror"
      error = "Animal nao encontrado."
    }

    db.get servico {
      field_name = "id"
      field_value = $input.servico_id
      output = ["id", "categoria", "duracao_minutos"]
    } as $servico

    precondition ($servico != null) {
      error_type = "inputerror"
      error = "Servico nao encontrado."
    }

    // D5: servico sem categoria nao e oferecido ao tutor, entao tambem nao
    // pode ser agendado por requisicao direta.
    precondition (($servico.categoria == "clinica") || ($servico.categoria == "banho_tosa")) {
      error_type = "inputerror"
      error = "Este servico nao esta disponivel para agendamento."
    }

    precondition ($servico.duracao_minutos > 0) {
      error_type = "inputerror"
      error = "Este servico nao esta disponivel para agendamento."
    }

    // Grade de 30 minutos. Vale no fuso de Sao Paulo porque o deslocamento
    // e de horas inteiras (D3).
    precondition (($input.inicio|modulus:1800000) == 0) {
      error_type = "inputerror"
      error = "O horario precisa ser de 30 em 30 minutos."
    }

    precondition ($input.inicio > ("now"|to_ms)) {
      error_type = "inputerror"
      error = "Escolha um horario no futuro."
    }

    // D1: o fim e gravado, com a duracao do servico neste momento.
    var $fim {
      value = $input.inicio + ($servico.duracao_minutos * 60000)
    }

    // D3: expediente no fuso da clinica, conferido pelo proprio Xano.
    // `N` e o dia da semana ISO (1 = segunda, 7 = domingo); `Hi` vira um
    // inteiro como 830 para 08:30.
    var $dia_semana {
      value = ($input.inicio|format_timestamp:"N":"America/Sao_Paulo")|to_int
    }

    var $hora_inicio {
      value = ($input.inicio|format_timestamp:"Hi":"America/Sao_Paulo")|to_int
    }

    var $hora_fim {
      value = ($fim|format_timestamp:"Hi":"America/Sao_Paulo")|to_int
    }

    var $fecha_as {
      value = 1800
    }

    conditional {
      if ($dia_semana == 6) {
        var.update $fecha_as {
          value = 1200
        }
      }
    }

    precondition ($dia_semana != 7) {
      error_type = "inputerror"
      error = "A clinica nao abre aos domingos."
    }

    precondition (($hora_inicio > 800) || ($hora_inicio == 800)) {
      error_type = "inputerror"
      error = "Fora do horario de funcionamento."
    }

    // O atendimento inteiro tem de caber. `mesmo dia` pega o fim que passa da
    // meia-noite, que como hora local viraria um numero pequeno e passaria
    // na comparacao com o fechamento.
    precondition (($fecha_as > $hora_fim) || ($fecha_as == $hora_fim)) {
      error_type = "inputerror"
      error = "O atendimento nao cabe no horario de funcionamento deste dia."
    }

    precondition (($input.inicio|format_timestamp:"Y-m-d":"America/Sao_Paulo") == ($fim|format_timestamp:"Y-m-d":"America/Sao_Paulo")) {
      error_type = "inputerror"
      error = "O atendimento nao cabe no horario de funcionamento deste dia."
    }

    // D5: a funcao vem da categoria, decidida aqui e nunca pelo cliente.
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

    // D4: a escolha e a gravacao acontecem dentro de uma transacao que TRAVA
    // as linhas dos profissionais compativeis. Uma segunda marcacao simultanea
    // para a mesma funcao espera esta terminar, e quando roda ja enxerga o
    // agendamento gravado aqui -- sem isso, as duas poderiam escolher o mesmo
    // profissional livre.
    db.transaction {
      stack {
        db.query colaborador {
          where = ($db.colaborador.ativo == true) && (($db.colaborador.funcao == $funcao_a) || ($db.colaborador.funcao == $funcao_b))
          sort = {id: "asc"}
          lock = true
          output = ["id"]
          return = {type: "list"}
        } as $profissionais

        var $escolhido {
          value = 0
        }

        // O primeiro livre no intervalo inteiro. Dois intervalos se cruzam
        // quando um comeca antes de o outro terminar; encostados (fim de um
        // == inicio do outro) nao se cruzam.
        foreach ($profissionais) {
          each as $profissional {
            conditional {
              if ($escolhido == 0) {
                db.query agendamento {
                  where = ($db.agendamento.id_colaborador == $profissional.id) && ($db.agendamento.situacao != "cancelado") && ($fim > $db.agendamento.inicio) && ($db.agendamento.fim > $input.inicio)
                  return = {type: "count"}
                } as $conflitos

                conditional {
                  if ($conflitos == 0) {
                    var.update $escolhido {
                      value = $profissional.id
                    }
                  }
                }
              }
            }
          }
        }

        precondition ($escolhido > 0) {
          error_type = "inputerror"
          error = "Este horario nao esta mais disponivel. Escolha outro."
        }

        db.add agendamento {
          data = {
            created_at    : "now"
            id_pet        : $animal.id
            id_servico    : $servico.id
            id_colaborador: $escolhido
            inicio        : $input.inicio
            fim           : $fim
            situacao      : "marcado"
            observacoes   : $input.observacoes
          }
        } as $novo
      }
    }
  }

  response = {
    id      : $novo.id
    inicio  : $novo.inicio
    fim     : $novo.fim
    situacao: $novo.situacao
  }
}
