// O catalogo que o tutor ve na agenda (change `agendamento`, spec de
// servicos: "O tutor le o catalogo").
//
// Leitura apenas, e so dos servicos com categoria (D5): servico antigo sem
// categoria continua na lista da equipe e fica fora daqui ate a clinica
// classifica-lo. Alterar o catalogo continua exclusivo dos `equipe_*`.
query servicos verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista os servicos agendaveis (com categoria) para o tutor"

  input {
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.query servico {
      where = ($db.servico.categoria == "clinica") || ($db.servico.categoria == "banho_tosa")
      sort = {nome: "asc"}
      output = ["id", "nome", "descricao", "preco", "duracao_minutos", "categoria"]
      return = {type: "list"}
    } as $catalogo
  }

  response = $catalogo
}
