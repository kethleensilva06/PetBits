// Atualiza um registro de produto; grava apenas os campos enviados na requisicao
query "produto/{produto_id}" verb=PATCH {
  api_group = "PetBits"

  input {
    int produto_id? filters=min:1
    dblink {
      table = "produto"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch produto {
      field_name = "id"
      field_value = $input.produto_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}