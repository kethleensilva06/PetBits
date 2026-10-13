// Cadastra um produto na loja (change `loja`).
//
// As recusas moram na pilha, antes da gravacao, no padrao do
// `equipe_servico_create.xs`: declaracao de coluna nao recusa preco zero nem
// estoque negativo. So operadores ja executados pelo motor nesta conta --
// `(> 0) || (== 0)` no lugar de `>= 0`, pelo motivo escrito naquele arquivo.
query "equipe/produtos" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cadastra um produto na loja"

  input {
    text nome filters=trim
    text descricao? filters=trim
    text categoria filters=trim
    text marca? filters=trim
    text unidade? filters=trim
    decimal preco
    int estoque
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

    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do produto nao pode ficar em branco."
    }

    // O enum barra o resto no banco, mas com 500 cru; aqui a recusa tem motivo.
    precondition (($input.categoria == "racao") || ($input.categoria == "petisco") || ($input.categoria == "brinquedo") || ($input.categoria == "higiene") || ($input.categoria == "acessorio") || ($input.categoria == "medicamento")) {
      error_type = "inputerror"
      error = "Categoria invalida."
    }

    precondition ($input.preco > 0) {
      error_type = "inputerror"
      error = "O preco do produto tem de ser maior que zero."
    }

    precondition (($input.estoque > 0) || ($input.estoque == 0)) {
      error_type = "inputerror"
      error = "O estoque nao pode ser negativo."
    }

    db.add produto {
      data = {
        created_at: "now"
        nome      : $input.nome
        descricao : $input.descricao
        categoria : $input.categoria
        marca     : $input.marca
        unidade   : $input.unidade
        preco     : $input.preco
        estoque   : $input.estoque
        ativo     : true
      }
    } as $novo
  }

  response = {
    id       : $novo.id
    nome     : $novo.nome
    descricao: $novo.descricao
    categoria: $novo.categoria
    marca    : $novo.marca
    unidade  : $novo.unidade
    preco    : $novo.preco
    estoque  : $novo.estoque
    ativo    : $novo.ativo
  }
}
