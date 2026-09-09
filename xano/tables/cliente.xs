table "cliente" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

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

    timestamp data_cadastro?=now {
      description = "Momento do cadastro"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "cpf", op: "asc"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}
