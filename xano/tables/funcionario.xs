table "funcionario" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

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
