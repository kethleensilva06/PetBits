// O historico de um animal, para a equipe (change `historico-clinico`, D3).
//
// Do quando mais recente para o mais antigo. De quem atendeu vao so o nome e
// a funcao, por `eval`: o contato do colaborador nao sai daqui. Quem esta
// retificado a tela calcula pelos `retifica` da propria lista -- o original
// nunca e tocado.
query "equipe/animais/{pet_id}/historico" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Atendimentos de um animal, do mais recente ao mais antigo, para a equipe"

  input {
    int pet_id filters=min:1
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

    db.query pet {
      where = $db.pet.id == $input.pet_id
      output = ["id"]
      return = {type: "single"}
    } as $animal

    precondition ($animal != null) {
      error_type = "notfound"
      error = "Animal nao encontrado."
    }

    db.query atendimento {
      join = {
        colaborador: {type: "left", table: "colaborador", where: $db.atendimento.id_colaborador == $db.colaborador.id}
      }

      where = $db.atendimento.id_pet == $animal.id
      eval = {
        colaborador_nome  : $db.colaborador.nome
        colaborador_funcao: $db.colaborador.funcao
      }

      sort = {data_atendimento: "desc"}
      output = ["id", "id_colaborador", "id_agendamento", "retifica", "data_atendimento", "motivo", "diagnostico", "tratamento", "peso", "retorno", "created_at", "colaborador_nome", "colaborador_funcao"]
      return = {type: "list"}
    } as $historico
  }

  response = $historico
}
