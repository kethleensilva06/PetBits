// Remove a foto enviada de um produto (change `foto-do-produto-na-mao`, D1).
//
// Mesma abertura de todo `equipe_*`, conferida pela guarda
// `scripts/verificar_equipe.py`. Remover e gravar `foto = null`: a loja ja cai,
// sozinha, na foto do proprio produto que acompanha o app e depois na da
// categoria (`imagem_do_produto`).
query "equipe/produtos/{produto_id}/foto" verb=DELETE {
  api_group = "PetBits"
  auth = "user"
  description = "Remove a foto enviada de um produto da loja"

  input {
    int produto_id filters=min:1
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
      where = $db.produto.id == $input.produto_id
      output = ["id"]
      return = {type: "single"}
    } as $existente

    precondition ($existente != null) {
      error_type = "notfound"
      error = "Produto nao encontrado."
    }

    db.patch produto {
      field_name = "id"
      field_value = $existente.id
      data = {foto: null}
    } as $atualizado
  }

  response = {id: $atualizado.id, foto: $atualizado.foto}
}
