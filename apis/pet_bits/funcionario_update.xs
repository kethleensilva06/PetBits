// Atualiza um registro de funcionario; grava apenas os campos enviados na requisicao
query "funcionario/{funcionario_id}" verb=PATCH {
  api_group = "PetBits"

  input {
    int funcionario_id? filters=min:1
    dblink {
      table = "funcionario"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch funcionario {
      field_name = "id"
      field_value = $input.funcionario_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}