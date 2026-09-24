// Atualiza um registro de pedido; envie apenas os campos que deseja alterar
query "pedido/{pedido_id}" verb=PATCH {
  api_group = "PetBits"

  input {
    int pedido_id? filters=min:1
    dblink {
      table = "pedido"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.patch pedido {
      field_name = "id"
      field_value = $input.pedido_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}
