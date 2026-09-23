// Lista todos os registros de agendamento
query agendamento verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query agendamento {
      sort = {data_hora: "desc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}