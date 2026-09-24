// Atualiza um registro de prontuario; apenas os campos enviados sao gravados
query "prontuario/{prontuario_id}" verb=PATCH {
  api_group = "PetBits"

  input {
    int prontuario_id? filters=min:1
    dblink {
      table = "prontuario"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch prontuario {
      field_name = "id"
      field_value = $input.prontuario_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}