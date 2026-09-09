table "servico" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

    text nome_servico filters=trim {
      description = "Nome do servico"
    }

    text descricao? filters=trim {
      description = "Descricao do servico"
    }

    decimal preco filters=min:0 {
      description = "Preco do servico"
    }

    int duracao_estimada? filters=min:0 {
      description = "Duracao estimada em minutos"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome_servico", op: "asc"}]}
  ]
}
