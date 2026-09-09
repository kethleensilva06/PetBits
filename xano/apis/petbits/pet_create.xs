query "pet" verb=POST {
  api_group = "petbits"
  description = "Cria um registro em pet"
  input {
    int id_cliente {
      description = "Tutor do pet"
    }

    text nome filters=trim {
      description = "Nome do pet"
    }

    text especie filters=trim {
      description = "Especie do pet"
    }

    text raca? filters=trim {
      description = "Raca do pet"
    }

    date data_nascimento? {
      description = "Data de nascimento"
    }

    decimal peso? {
      description = "Peso em quilos"
    }

    text observacoes? filters=trim {
      description = "Observacoes gerais"
    }
  }
  stack {
    db.add "pet" {
      data = {
        id_cliente: $input.id_cliente,
        nome: $input.nome,
        especie: $input.especie,
        raca: $input.raca,
        data_nascimento: $input.data_nascimento,
        peso: $input.peso,
        observacoes: $input.observacoes
      }
    } as $registro
  }
  response = $registro
}
