// Uma linha do pedido (change `loja`, D1).
//
// `preco_unitario` e `produto_nome` sao CONGELADOS na hora da compra (modelo de
// dominio): mudar o preco ou o nome do produto nao reescreve o historico de
// vendas. `valor_linha` e calculado no servidor.
table pedido_item {
  auth = false

  schema {
    int id

    int id_pedido {
      table = "pedido"
    }

    int id_produto {
      table = "produto"
    }

    text produto_nome
    int quantidade
    decimal preco_unitario
    decimal valor_linha

    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pedido", op: "asc"}]}
    {type: "btree", field: [{name: "id_produto", op: "asc"}]}
  ]
}
