// O historico de um animal do tutor autenticado (change `historico-clinico`, D3).
//
// A posse e provada como no `pet/{pet_id}`: o animal e procurado com o dono
// vindo do token, e animal alheio sai igual a animal inexistente. De quem
// atendeu vao so o nome e a funcao -- o contato do colaborador e interno
// (spec `colaboradores`). Quem registrou (`registrado_por`) tambem nao sai.
query "pet/{pet_id}/historico" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Atendimentos de um animal do tutor autenticado, do mais recente ao mais antigo"

  input {
    int pet_id filters=min:1
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.query pet {
      join = {
        tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
      }

      where = ($db.pet.id == $input.pet_id) && ($db.tutor.id_user == $auth.id)
      output = ["id"]
      return = {type: "single"}
    } as $meu

    precondition ($meu != null) {
      error_type = "notfound"
      error = "Animal nao encontrado."
    }

    db.query atendimento {
      join = {
        colaborador: {type: "left", table: "colaborador", where: $db.atendimento.id_colaborador == $db.colaborador.id}
      }

      where = $db.atendimento.id_pet == $meu.id
      eval = {
        colaborador_nome  : $db.colaborador.nome
        colaborador_funcao: $db.colaborador.funcao
      }

      sort = {data_atendimento: "desc"}
      output = ["id", "retifica", "data_atendimento", "motivo", "diagnostico", "tratamento", "peso", "retorno", "colaborador_nome", "colaborador_funcao"]
      return = {type: "list"}
    } as $historico
  }

  response = $historico
}
