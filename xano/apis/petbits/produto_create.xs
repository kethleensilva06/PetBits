query "produto" verb=POST {
  api_group = "petbits"
  description = "Cria um registro em produto"
  input {
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

    decimal preco_venda {
      description = "Preco de venda"
    }
  }
  stack {
    db.add "produto" {
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
