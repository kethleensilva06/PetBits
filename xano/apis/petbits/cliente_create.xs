query "cliente" verb=POST {
  api_group = "petbits"
  description = "Cria um registro em cliente"
  input {
    text nome filters=trim {
      description = "Nome completo do tutor"
    }

    text cpf filters=trim {
      description = "CPF do tutor"
    }

    text email? filters=trim {
      description = "E-mail de contato"
    }

    text telefone? filters=trim {
      description = "Telefone de contato"
    }

    text endereco? filters=trim {
      description = "Endereco do tutor"
    }
  }
  stack {
    db.add "cliente" {
      data = {
        nome: $input.nome,
        cpf: $input.cpf,
        email: $input.email,
        telefone: $input.telefone,
        endereco: $input.endereco
      }
    } as $registro
  }
  response = $registro
}
