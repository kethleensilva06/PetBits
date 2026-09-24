// Atualiza um registro de itens_pedido; grava apenas os campos enviados na requisicao
query "itens_pedido/{itens_pedido_id}" verb=PATCH {
  api_group = "PetBits"

  input {
    int itens_pedido_id? filters=min:1
    dblink {
      table = "itens_pedido"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.patch itens_pedido {
      field_name = "id"
      field_value = $input.itens_pedido_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}
