// Atualiza apenas os campos enviados de um registro de cliente
query "cliente/{cliente_id}" verb=PATCH {
  api_group = "PetBits"

  // Ver a nota em cliente_create.xs: id_user nunca entra pelo corpo da
  // requisicao. Aqui o risco e maior, porque reapontar uma ficha ja existente
  // para outro login e o ataque direto.
  input {
    int cliente_id? filters=min:1
    dblink {
      table = "cliente"
      override = {
        id_user: {hidden: true}
      }
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch cliente {
      field_name = "id"
      field_value = $input.cliente_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $registro
  }

  response = $registro
}