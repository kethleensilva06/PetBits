// Altera um servico do catalogo da clinica.
//
// Padrao `pick` do `pet_update.xs`: o corpo CRU diz quais campos a requisicao
// de fato enviou, e so esses sao tocados. Sem isso, um campo ausente chegaria
// em `$input` como o padrao do tipo ("" ou 0) e uma edicao de preco apagaria a
// descricao e zeraria a duracao -- "os campos nao mencionados permanecem" tem
// de ser estrutural, nao disciplina de quem chama.
//
// E AQUI ESTA O CASO SUTIL QUE O `pick` TORNA POSSIVEL (design.md, D10):
// `duracao_minutos: 0` nao e campo omitido, e valor INFORMADO. A chave existe
// no corpo cru, entao ela passa pelo `pick` e chega na gravacao. Duas
// consequencias que decidem a forma das guardas abaixo:
//
//   1. A guarda tem de rodar sobre `$dados` -- o que VAI SER GRAVADO --, nunca
//      sobre `$input`. Uma `precondition ($input.duracao_minutos > 0)` solta na
//      pilha recusaria toda edicao parcial que nao mencionasse a duracao,
//      porque o campo ausente chega como 0. O bug inverso, e silencioso: a tela
//      funciona, a requisicao direta nao.
//   2. A guarda tem de rodar ANTES da gravacao. Ela lanca, nada e escrito, e a
//      duracao anterior permanece -- que e literalmente o segundo THEN do
//      cenario "duracao nao pode ser zerada na alteracao".
//
// `db.patch` recusa `where` e `join` (fato medido 4), entao a existencia e
// conferida por uma consulta propria e so depois a acao acontece.
//
// SEM transacao com lock, ao contrario do `pet_update.xs`, e a diferenca tem
// motivo: la a consulta prova POSSE, e a janela entre provar e gravar e onde a
// posse poderia mudar. Aqui ela prova so EXISTENCIA, e o que vai ser gravado
// nao vem da linha lida, vem do corpo da requisicao -- o lock nao protegeria
// nada, e transacao interrompida antes do commit deixa a linha presa, o que ja
// foi medido. Mesma forma do `equipe_colaborador_update.xs`.
query "equipe/servicos/{servico_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"
  description = "Altera um servico do catalogo da clinica"

  input {
    int servico_id filters=min:1
    text nome? filters=trim
    text descricao? filters=trim
    decimal preco?
    int duracao_minutos?
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

    // `servico_id` sai fora: ele vem do caminho, nao do corpo, e nao e campo
    // alteravel. O `unset` e defesa contra o dia em que alguem o mandar no
    // corpo tambem.
    var $dados {
      value = `$input|pick:($corpo_cru|keys)`|unset:"servico_id"
    }

    precondition (($dados|count) > 0) {
      error_type = "inputerror"
      error = "Informe ao menos um campo para alterar."
    }

    // Condicional porque a edicao e parcial: quem nao envia o campo nao o esta
    // esvaziando. Quem envia so espacos, esta.
    conditional {
      if (($dados|has:"nome") == true) {
        precondition ((($dados|get:"nome")|trim) != "") {
          error_type = "inputerror"
          error = "O nome do servico nao pode ficar em branco."
        }
      }
    }

    // O cenario proprio da spec. `has` distingue "nao mandou" de "mandou 0", e
    // e essa distincao que faz a guarda recusar o zero sem recusar a edicao que
    // nem fala de duracao.
    conditional {
      if (($dados|has:"duracao_minutos") == true) {
        precondition (($dados|get:"duracao_minutos") > 0) {
          error_type = "inputerror"
          error = "A duracao do servico tem de ser maior que zero."
        }
      }
    }

    // Mesma forma, limite diferente: aqui o zero PASSA. Servico gratuito e
    // valido na alteracao pelo mesmo motivo que e valido na criacao.
    //
    // `(> 0) || (== 0)` em vez de `>= 0` pelo motivo que esta por extenso no
    // `equipe_servico_create.xs`: `>=` nunca foi executado pelo motor nesta
    // conta, e o parser aceitar nao prova nada (ele aceita `===`, fato medido
    // 2). Os dois arquivos mudam juntos, ou um deles vira o contra-exemplo.
    conditional {
      if (($dados|has:"preco") == true) {
        precondition ((($dados|get:"preco") > 0) || (($dados|get:"preco") == 0)) {
          error_type = "inputerror"
          error = "O preco do servico nao pode ser negativo."
        }
      }
    }

    db.query servico {
      where = $db.servico.id == $input.servico_id
      output = ["id"]
      return = {type: "single"}
    } as $existente

    precondition ($existente != null) {
      error_type = "notfound"
      error = "Servico nao encontrado."
    }

    // Pelo id que a CONSULTA devolveu, nunca pelo id da requisicao. Aqui os
    // dois sao iguais por construcao; a forma fica igual a do `pet_update.xs`
    // para que copiar este arquivo como modelo de uma escrita COM dono nao
    // perca justamente a parte que importa.
    db.patch servico {
      field_name = "id"
      field_value = $existente.id
      data = $dados
    } as $atualizado
  }

  response = {
    id             : $atualizado.id
    nome           : $atualizado.nome
    descricao      : $atualizado.descricao
    preco          : $atualizado.preco
    duracao_minutos: $atualizado.duracao_minutos
  }
}
