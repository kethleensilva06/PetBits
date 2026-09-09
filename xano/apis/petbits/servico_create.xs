query "servico" verb=POST {
  api_group = "petbits"
  description = "Cria um registro em servico"
  input {
    text nome_servico filters=trim {
      description = "Nome do servico"
    }

    text descricao? filters=trim {
      description = "Descricao do servico"
    }

    decimal preco {
      description = "Preco do servico"
    }

    int duracao_estimada? {
      description = "Duracao estimada em minutos"
    }
  }
  stack {
    db.add "servico" {
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
