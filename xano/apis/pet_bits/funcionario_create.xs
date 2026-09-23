query "funcionario" verb=POST {
  api_group = "PetBits"
  description = "Cria um registro em funcionario"
  input {
    text nome filters=trim {
      description = "Nome do colaborador"
    }

    text cpf filters=trim {
      description = "CPF do colaborador"
    }

    text cargo filters=trim {
      description = "veterinario, tosador ou atendente"
    }

    text telefone? filters=trim {
      description = "Telefone de contato"
    }

    text email? filters=trim {
      description = "E-mail de contato"
    }

    date data_contratacao? {
      description = "Data de contratacao"
    }
  }
  stack {
    db.add "funcionario" {
      data = {
        nome: $input.nome,
        cpf: $input.cpf,
        cargo: $input.cargo,
        telefone: $input.telefone,
        email: $input.email,
        data_contratacao: $input.data_contratacao
      }
    } as $registro
  }
  response = $registro
}
