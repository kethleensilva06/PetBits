table "pet" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

    int id_cliente {
      table = "cliente"
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

    decimal peso? filters=min:0 {
      description = "Peso em quilos"
    }

    text observacoes? filters=trim {
      description = "Observacoes gerais"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_cliente", op: "asc"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}
