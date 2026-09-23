// Query all Teste records
query teste verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query Teste {
      return = {type: "list"}
    } as $teste
  }

  response = $teste
}