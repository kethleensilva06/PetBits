// O que o cliente pode comprar (change `loja`, spec de produtos): ativos com
// estoque maior que zero. Leitura apenas -- o catalogo e da equipe.
query "loja/produtos" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista os produtos a venda na loja"

  input {
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.query produto {
      where = ($db.produto.ativo == true) && ($db.produto.estoque > 0)
      sort = {nome: "asc"}
      output = ["id", "nome", "descricao", "categoria", "marca", "unidade", "preco", "estoque"]
      return = {type: "list"}
    } as $vitrine
  }

  response = $vitrine
}
