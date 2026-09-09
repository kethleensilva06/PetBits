query "servico/{id}" verb=PATCH {
  api_group = "petbits"
  description = "Substitui os campos de um registro de servico; envie o registro completo"
  input {
    int id {
      description = "Identificador do registro"
    }

    text nome_servico? filters=trim {
      description = "Nome do servico"
    }

    text descricao? filters=trim {
      description = "Descricao do servico"
    }

    decimal preco? {
      description = "Preco do servico"
    }

    int duracao_estimada? {
      description = "Duracao estimada em minutos"
    }
  }
  stack {
    db.edit "servico" {
      field_name = "id"
      field_value = $input.id
      data = {
        nome_servico: $input.nome_servico,
        descricao: $input.descricao,
        preco: $input.preco,
        duracao_estimada: $input.duracao_estimada
      }
    } as $registro
  }
  response = $registro
}
