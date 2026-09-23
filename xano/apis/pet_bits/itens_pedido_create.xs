query "itens_pedido" verb=POST {
  api_group = "PetBits"
  description = "Cria um registro em itens_pedido"
  input {
    int id_pedido {
      description = "Pedido ao qual o item pertence"
    }

    int id_produto {
      description = "Produto vendido"
    }

    int quantidade {
      description = "Quantidade vendida"
    }

    decimal valor_unitario {
      description = "Preco unitario no momento da venda"
    }

    decimal valor_total {
      description = "Quantidade multiplicada pelo valor unitario"
    }
  }
  stack {
    db.add "itens_pedido" {
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
