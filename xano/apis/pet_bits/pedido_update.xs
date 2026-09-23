query "pedido/{id}" verb=PATCH {
  api_group = "PetBits"
  description = "Substitui os campos de um registro de pedido; envie o registro completo"
  input {
    int id {
      description = "Identificador do registro"
    }

    int id_cliente? {
      description = "Cliente do pedido"
    }

    text status? filters=trim {
      description = "pendente, pago, enviado ou entregue"
    }

    decimal valor_total? {
      description = "Soma dos itens do pedido"
    }
  }
  stack {
    db.edit "pedido" {
      field_name = "id"
      field_value = $input.id
      data = {
        id_cliente: $input.id_cliente,
        status: $input.status,
        valor_total: $input.valor_total
      }
    } as $registro
  }
  response = $registro
}
