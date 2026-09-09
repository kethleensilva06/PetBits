query "prontuario" verb=GET {
  api_group = "petbits"
  description = "Lista todos os registros de prontuario"
  input {
  }
  stack {
    db.query "prontuario" {
      sort = {data_atendimento: "desc"}
      return = {type: "list"}
    } as $registros
  }
  response = $registros
}
