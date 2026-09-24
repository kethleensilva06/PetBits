// Atualiza um registro de agendamento; apenas os campos enviados sao gravados
query "agendamento/{agendamento_id}" verb=PATCH {
  api_group = "PetBits"

  input {
    int agendamento_id? filters=min:1
    dblink {
      table = "agendamento"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.patch agendamento {
      field_name = "id"
      field_value = $input.agendamento_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}
