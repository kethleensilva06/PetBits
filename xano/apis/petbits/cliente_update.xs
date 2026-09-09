query "cliente/{id}" verb=PATCH {
  api_group = "petbits"
  description = "Substitui os campos de um registro de cliente; envie o registro completo"
  input {
    int id {
      description = "Identificador do registro"
    }

    text nome? filters=trim {
      description = "Nome completo do tutor"
    }

    text cpf? filters=trim {
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
    db.edit "cliente" {
      field_name = "id"
      field_value = $input.id
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
