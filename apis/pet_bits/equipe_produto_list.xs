// O catalogo da loja inteiro, ativos e inativos, para a equipe (change `loja`).
//
// Mesma abertura de todo `equipe_*`, conferida pela guarda
// `scripts/verificar_equipe.py`: `produto` nao tem coluna de dono, entao sem a
// prova esta consulta entregaria o catalogo -- e o estoque -- a qualquer conta.
query "equipe/produtos" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista todos os produtos da loja, para a equipe"

  input {
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    db.query produto {
      sort = {nome: "asc"}
      output = ["id", "nome", "descricao", "categoria", "marca", "unidade", "preco", "estoque", "ativo"]
      return = {type: "list"}
    } as $produtos
  }

  response = $produtos
}
