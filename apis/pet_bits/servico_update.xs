// Substitui os campos de um registro de servico; envie o registro completo
query "servico/{id}" verb=PATCH {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  
    // Nome do servico
    text nome_servico? filters=trim
  
    // Descricao do servico
    text descricao? filters=trim
  
    // Preco do servico
    decimal preco?
  
    // Duracao estimada em minutos
    int duracao_estimada?
  }

  stack {
    db.edit servico {
      field_name = "id"
      field_value = $input.id
      data = {
        nome_servico    : $input.nome_servico
        descricao       : $input.descricao
        preco           : $input.preco
        duracao_estimada: $input.duracao_estimada
      }
    } as $registro
  }

  response = $registro
}