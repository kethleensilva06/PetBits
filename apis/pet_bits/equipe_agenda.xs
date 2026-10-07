// A agenda de um dia, para a equipe (change `agendamento`, D8). So leitura.
//
// Mesma abertura de todo `equipe_*`, conferida pela guarda
// `scripts/verificar_equipe.py`: sem a prova, esta consulta devolveria a
// agenda da clinica inteira para qualquer conta logada.
//
// O telefone do tutor sai porque a equipe ja o le em `equipe/tutores` e
// precisa dele para avisar de um atraso. Documento e endereco, nao.
query "equipe/agenda" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Agendamentos de um dia, de todos os profissionais, para a equipe"

  input {
    // Inicio do dia (meia-noite em Sao Paulo), em ms UTC.
    timestamp dia
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

    var $fim_do_dia {
      value = $input.dia + 86400000
    }

    db.query agendamento {
      join = {
        pet        : {type: "left", table: "pet", where: $db.agendamento.id_pet == $db.pet.id}
        tutor      : {type: "left", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
        servico    : {type: "left", table: "servico", where: $db.agendamento.id_servico == $db.servico.id}
        colaborador: {type: "left", table: "colaborador", where: $db.agendamento.id_colaborador == $db.colaborador.id}
      }

      where = (($db.agendamento.inicio > $input.dia) || ($db.agendamento.inicio == $input.dia)) && ($fim_do_dia > $db.agendamento.inicio)
      eval = {
        pet_nome         : $db.pet.nome
        pet_especie      : $db.pet.especie
        tutor_nome       : $db.tutor.nome
        tutor_telefone   : $db.tutor.telefone
        servico_nome     : $db.servico.nome
        profissional_nome: $db.colaborador.nome
      }

      sort = {inicio: "asc"}
      output = ["id", "inicio", "fim", "situacao", "observacoes", "pet_nome", "pet_especie", "tutor_nome", "tutor_telefone", "servico_nome", "profissional_nome"]
      return = {type: "list"}
    } as $agenda
  }

  response = $agenda
}
