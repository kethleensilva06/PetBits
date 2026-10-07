// Cadastra um servico no catalogo da clinica.
//
// Mesma abertura das leituras: a prova de equipe antes de qualquer db.* -- e
// aqui ela importa mais, porque uma escrita sem prova nao devolve dado alheio,
// ela ALTERA o catalogo de todo mundo e deixa o registro do estrago.
//
// As tres recusas abaixo sao o que o D10 chama de "o que o parser nao cobra":
// nenhuma declaracao de coluna garante nome nao vazio, duracao positiva ou
// preco nao negativo. `decimal preco` aceita -10 e `int duracao_minutos`
// aceita 0 sem reclamar. Entao as guardas moram na pilha, antes da gravacao, e
// cada uma devolve mensagem propria -- a spec pede que o motivo seja
// informado, e um 500 cru do motor nao informa nada.
//
// O ZERO e o ponto a nao errar aqui, e ele e assimetrico entre os dois campos:
// preco zero e VALIDO (servico gratuito e cenario explicito da spec) e duracao
// zero e INVALIDA (sem duracao nao ha como saber se dois atendimentos se
// sobrepoem, que e a razao de a coluna existir).
query "equipe/servicos" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cria um servico no catalogo da clinica"

  // `db.add` exige `data` como objeto LITERAL -- so `db.patch` aceita
  // variavel. Por isso cada campo e referenciado diretamente la embaixo, e por
  // isso o tipo declarado aqui e o que de fato chega na gravacao.
  //
  // `descricao` e o unico opcional: a spec tem cenario proprio dizendo que
  // cadastro sem descricao e criado normalmente.
  input {
    text nome filters=trim
    text descricao? filters=trim
    decimal preco
    int duracao_minutos
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

    // `filters=trim` reduz "   " a string vazia DEPOIS de a obrigatoriedade da
    // entrada ser satisfeita -- a chave esta presente, entao o Xano aceita.
    // Sem esta guarda, nasce servico sem nome por requisicao direta; foi assim
    // que a change anterior encontrou POST aceitando animal so de espacos.
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do servico nao pode ficar em branco."
    }

    // Maior que zero, nao "maior ou igual": duracao zerada e o que torna a
    // agenda incalculavel.
    precondition ($input.duracao_minutos > 0) {
      error_type = "inputerror"
      error = "A duracao do servico tem de ser maior que zero."
    }

    // Maior OU IGUAL a zero: o zero passa de proposito. Trocar isto por `> 0`
    // recusaria o servico gratuito, que a spec exige aceitar.
    //
    // Escrito como `(> 0) || (== 0)` e NAO como `>= 0`, e isto e deliberado:
    // `>=` nao aparece em nenhum outro `.xs` deste repositorio, entao o motor
    // do Xano nunca o executou nesta conta. O parser aceitar nao basta -- ele
    // aceita `===`, que o motor recusa com ERROR_FATAL (fato medido 2). `>`,
    // `==` e `||` ja rodam em producao aqui. E a forma provada, nao a bonita
    // (design.md, D8), e o preco 0 da tarefa 5.2 e justamente a requisicao que
    // cairia nesta linha. Se um dia `>=` for medido num endpoint descartavel,
    // esta expressao pode encolher -- com a medicao registrada no design.
    precondition (($input.preco > 0) || ($input.preco == 0)) {
      error_type = "inputerror"
      error = "O preco do servico nao pode ser negativo."
    }

    // `created_at` vai LITERAL, como em `pet_create.xs`, `tutor_cadastro.xs` e
    // `equipe_colaborador_create.xs` -- este era o unico `db.add` do projeto
    // sem ele. A coluna EXISTE em `tables/servico.xs` (`timestamp
    // created_at?=now`), igual a de `pet` e a de `colaborador`; a versao
    // anterior deste arquivo afirmava o contrario, e a afirmacao estava errada.
    //
    // Ter padrao na coluna nao dispensa mandar o valor: que o padrao dispare no
    // insert nunca foi observado neste projeto, e e a razao escrita no
    // `equipe_colaborador_create.xs` para o `ativo: true` ir literal mesmo com
    // `?=true` declarado. Se nao disparar, todo servico nasce sem data de
    // criacao e nada acusa -- a familia de falha silenciosa que o D8 manda
    // evitar. Mandar custa nada e esta certo nos dois mundos.
    db.add servico {
      data = {
        created_at     : "now"
        nome           : $input.nome
        descricao      : $input.descricao
        preco          : $input.preco
        duracao_minutos: $input.duracao_minutos
      }
    } as $novo
  }

  // Montada campo a campo, com o mesmo conjunto de chaves da listagem: assim
  // uma coluna interna acrescentada a tabela depois nao comeca a sair na
  // resposta da criacao sem ninguem decidir isso.
  response = {
    id             : $novo.id
    nome           : $novo.nome
    descricao      : $novo.descricao
    preco          : $novo.preco
    duracao_minutos: $novo.duracao_minutos
  }
}
