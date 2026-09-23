table "produto" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

    text nome filters=trim {
      description = "Nome do produto"
    }

    text categoria? filters=trim {
      description = "Categoria do produto"
    }

    text marca? filters=trim {
      description = "Marca do produto"
    }

    text unidade? filters=trim {
      description = "Unidade de medida"
    }

    decimal preco_venda filters=min:0 {
      description = "Preco de venda"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}
