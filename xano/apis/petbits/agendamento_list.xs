query "agendamento" verb=GET {
  api_group = "petbits"
  description = "Lista todos os registros de agendamento"
  input {
  }
  stack {
    db.query "agendamento" {
      sort = {data_hora: "desc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
