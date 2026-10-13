// Os agendamentos dos animais do tutor autenticado.
//
// Padrao de LEITURA da change `animais-do-tutor` (D1): a consulta ja nasce
// filtrada pelo join agendamento -> pet -> tutor -> conta. Nao existe instante
// em que um agendamento alheio esteja numa variavel deste endpoint.
//
// Do profissional saem nome e funcao, e nada mais: o modelo de dominio diz
// que o tutor precisa saber quem atende o animal, e que contato e documento
// de colaborador sao internos.
query agendamentos verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista os agendamentos dos animais do tutor autenticado"

  input {
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.query agendamento {
      join = {
        pet        : {type: "inner", table: "pet", where: $db.agendamento.id_pet == $db.pet.id}
        tutor      : {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
        servico    : {type: "left", table: "servico", where: $db.agendamento.id_servico == $db.servico.id}
        colaborador: {type: "left", table: "colaborador", where: $db.agendamento.id_colaborador == $db.colaborador.id}
      }

      where = $db.tutor.id_user == $auth.id
      eval = {
        pet_nome          : $db.pet.nome
        servico_nome      : $db.servico.nome
        servico_categoria : $db.servico.categoria
        profissional_nome : $db.colaborador.nome
        profissional_funcao: $db.colaborador.funcao
      }

      sort = {inicio: "desc"}
      output = ["id", "inicio", "fim", "situacao", "observacoes", "pet_nome", "servico_nome", "servico_categoria", "profissional_nome", "profissional_funcao"]
      return = {type: "list"}
    } as $meus
  }

  response = $meus
}
