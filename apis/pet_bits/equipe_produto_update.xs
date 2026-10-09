// Altera um produto da loja, inclusive estoque e ativo (change `loja`).
//
// Padrao `pick` do `equipe_servico_update.xs`: so os campos presentes no corpo
// cru sao tocados, e as guardas rodam sobre `$dados` -- o que VAI ser gravado
// --, nunca sobre `$input`, em que um campo ausente chega como 0 ou "".
query "equipe/produtos/{produto_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"
  description = "Altera um produto da loja"

  input {
    int produto_id filters=min:1
    text nome? filters=trim
    text descricao? filters=trim
    text categoria? filters=trim
    text marca? filters=trim
    text unidade? filters=trim
    decimal preco?
    int estoque?
    bool ativo?
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

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $corpo_cru

    var $dados {
      value = `$input|pick:($corpo_cru|keys)`|unset:"produto_id"
    }

    precondition (($dados|count) > 0) {
      error_type = "inputerror"
      error = "Informe ao menos um campo para alterar."
    }

    conditional {
      if (($dados|has:"nome") == true) {
        precondition ((($dados|get:"nome")|trim) != "") {
          error_type = "inputerror"
          error = "O nome do produto nao pode ficar em branco."
        }
      }
    }

    conditional {
      if (($dados|has:"categoria") == true) {
        precondition ((($dados|get:"categoria") == "racao") || (($dados|get:"categoria") == "petisco") || (($dados|get:"categoria") == "brinquedo") || (($dados|get:"categoria") == "higiene") || (($dados|get:"categoria") == "acessorio") || (($dados|get:"categoria") == "medicamento")) {
          error_type = "inputerror"
          error = "Categoria invalida."
        }
      }
    }

    conditional {
      if (($dados|has:"preco") == true) {
        precondition (($dados|get:"preco") > 0) {
          error_type = "inputerror"
          error = "O preco do produto tem de ser maior que zero."
        }
      }
    }

    conditional {
      if (($dados|has:"estoque") == true) {
        precondition ((($dados|get:"estoque") > 0) || (($dados|get:"estoque") == 0)) {
          error_type = "inputerror"
          error = "O estoque nao pode ser negativo."
        }
      }
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
      data = $dados
    } as $atualizado
  }

  response = {
    id       : $atualizado.id
    nome     : $atualizado.nome
    descricao: $atualizado.descricao
    categoria: $atualizado.categoria
    marca    : $atualizado.marca
    unidade  : $atualizado.unidade
    preco    : $atualizado.preco
    estoque  : $atualizado.estoque
    ativo    : $atualizado.ativo
  }
}
