// O catalogo da loja (change `loja`, D1). Mantido pela equipe.
//
// Como `servico`, nenhuma coluna aponta para dono: o catalogo e da clinica, e
// a unica recusa de escrita e a prova `PetBits/exige_equipe` em todo
// `equipe_produto_*`.
//
// O estoque e a unica coluna que o cliente MEXE, e so por um caminho: o
// `POST pedidos`, que baixa o estoque dentro de uma transacao com trava. As
// recusas de preco e estoque moram nas preconditions, nao aqui -- declaracao
// de coluna nao recusa nada (fato medido na change `operacao-da-clinica`).
table produto {
  auth = false

  schema {
    int id

    text nome filters=trim
    text descricao? filters=trim

    enum categoria {
      values = ["racao", "petisco", "brinquedo", "higiene", "acessorio", "medicamento"]
    }

    text marca? filters=trim

    // Texto livre: "un", "pacote 1 kg", "frasco 500 ml"
    text unidade? filters=trim

    decimal preco
    int estoque

    // Desativar tira da loja sem apagar: os itens de pedido antigos continuam
    // apontando para ele.
    bool ativo?=true

    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
    {type: "btree", field: [{name: "ativo", op: "asc"}, {name: "nome", op: "asc"}]}
  ]
}
