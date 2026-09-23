query "pedido" verb=POST {
  api_group = "PetBits"
  description = "Cria um registro em pedido"
  input {
    int id_cliente {
      description = "Cliente do pedido"
    }

    text status filters=trim {
      description = "pendente, pago, enviado ou entregue"
    }

    decimal valor_total? {
      description = "Soma dos itens do pedido"
    }
  }
  stack {
    db.add "pedido" {
      data = {
        id_cliente: $input.id_cliente,
        status: $input.status,
        valor_total: $input.valor_total
      }
    } as $registro
  }
  response = $registro
}
