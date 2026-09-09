query "itens_pedido/{id}" verb=PATCH {
  api_group = "petbits"
  description = "Substitui os campos de um registro de itens_pedido; envie o registro completo"
  input {
    int id {
      description = "Identificador do registro"
    }

    int id_pedido? {
      description = "Pedido ao qual o item pertence"
    }

    int id_produto? {
      description = "Produto vendido"
    }

    int quantidade? {
      description = "Quantidade vendida"
    }

    decimal valor_unitario? {
      description = "Preco unitario no momento da venda"
    }

    decimal valor_total? {
      description = "Quantidade multiplicada pelo valor unitario"
    }
  }
  stack {
    db.edit "itens_pedido" {
      field_name = "id"
      field_value = $input.id
      data = {
        id_pedido: $input.id_pedido,
        id_produto: $input.id_produto,
        quantidade: $input.quantidade,
        valor_unitario: $input.valor_unitario,
        valor_total: $input.valor_total
      }
    } as $registro
  }
  response = $registro
}
