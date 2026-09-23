// Lista todos os registros de prontuario
query prontuario verb=GET {
  api_group = "PetBits"

  input {
  }

  stack {
    db.query prontuario {
      sort = {data_atendimento: "desc"}
      return = {type: "list"}
    } as $registros
  }

  response = $registros
}