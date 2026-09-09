query "produto/{id}" verb=PATCH {
  api_group = "petbits"
  description = "Substitui os campos de um registro de produto; envie o registro completo"
  input {
    int id {
      description = "Identificador do registro"
    }

    text nome? filters=trim {
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

    decimal preco_venda? {
      description = "Preco de venda"
    }
  }
  stack {
    db.edit "produto" {
      field_name = "id"
      field_value = $input.id
      data = {
        nome: $input.nome,
        categoria: $input.categoria,
        marca: $input.marca,
        unidade: $input.unidade,
        preco_venda: $input.preco_venda
      }
    } as $registro
  }
  response = $registro
}
