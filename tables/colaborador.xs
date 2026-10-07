// Quem trabalha na clinica. E registro do DOMINIO, nao credencial: cadastrar
// um colaborador nao cria conta de acesso nem concede permissao nenhuma, e
// varios colaboradores sem conta coexistem (spec de colaboradores).
//
// NENHUMA coluna aponta para `user` ou para `tutor`, e isso e decisao, nao
// esquecimento (design.md, D2). A consequencia tem os dois lados, e quem
// mexer nesta tabela precisa saber os dois: nao existe coluna de dono, logo
// nao ha `where` de posse para alguem esquecer numa consulta -- e, em troca,
// a unica recusa desta superficie e a chamada a `PetBits/exige_equipe` no
// topo da pilha. Se ela sumir de um endpoint, `db.query colaborador` devolve
// a tabela inteira para qualquer conta autenticada, isto e, para qualquer
// visitante que se cadastrou. E por isso que a prova vem ANTES de qualquer
// db.*, e por isso existe a guarda de repositorio (design.md, D9).
//
// Como nao ha coluna de vinculo, nao se coloca aqui a pergunta que travou o
// indice de `tutor.id_user`: o Xano gravar 0 no lugar de um vinculo omitido
// nao tem onde morder nesta tabela.
table colaborador {
  auth = false

  schema {
    int id

    // Nome de quem trabalha na clinica
    text nome filters=trim

    // Conjunto fechado, exatamente estes tres valores (spec de
    // colaboradores). O enum barra o resto no banco, mas quem devolve a
    // recusa LEGIVEL e a precondition do endpoint de cadastro: um valor fora
    // do conjunto que chegue ao db.add vira 500 cru, e a spec pede que o
    // motivo seja informado (design.md, D10).
    enum funcao {
      values = ["gerente", "veterinario", "tosador", "atendente"]
    }

    // Contato -- opcional, porque a spec exige so nome e funcao, e o cadastro
    // sem contato e sem data de entrada tem cenario proprio.
    text telefone? filters=trim

    // O `?` fica depois do NOME: e nessa posicao que o parser le "opcional".
    // Em `tutor.xs` e em `898256_user.xs` ele aparece depois do TIPO, que e
    // outra coisa (nulavel) e veio copiado do template.
    email email? filters=trim|lower

    // `timestamp`, e nao `date`, por limitacao medida do Xano -- e o que foi
    // medido e o INPUT, nao a coluna: um input declarado a mao com tipo `date`
    // derruba o endpoint com 500 "Unable to locate input" quando o campo e
    // OMITIDO, mesmo declarado opcional e mesmo com valor padrao (a mesma nota
    // esta em pet.xs). A coluna acompanha o tipo do input por simetria, e
    // porque a tarefa 2.1 manda; que uma COLUNA `date` tenha o mesmo defeito e
    // inferencia por analogia, nao medicao. Este e justamente o campo que mais
    // vai faltar no cadastro feito as pressas no balcao, entao o tipo que
    // tolera a ausencia e o unico aceitavel aqui.
    timestamp data_entrada?

    // Desligamento sem perder o registro -- o historico de atendimento vai
    // apontar para o colaborador depois.
    //
    // `ativo` marca o ESTADO, nao esconde a linha: a spec de colaboradores
    // pede "todos os colaboradores cadastrados" na lista, e
    // `equipe_colaborador_list.xs` deixa escrito que nao filtra por esta
    // coluna de proposito. Quem acrescentar `where ativo == true` ali quebra
    // esse cenario -- e some tambem o unico caminho de religar alguem.
    //
    // O `?` nao e "campo sem importancia": e o que permite ao insert OMITIR a
    // coluna e cair no padrao. E a mesma forma de `created_at?=now`, a unica
    // com uso provado neste projeto. Mas o padrao aqui e rede, nao mecanismo:
    // `equipe_colaborador_create.xs` manda `ativo: true` LITERAL, porque o
    // padrao disparando no insert nunca foi observado nesta conta. Se o schema
    // publicado vier sem padrao, nada quebra hoje; o que se perde e a rede.
    bool ativo?=true

    timestamp created_at?=now
  }

  // A lista ordenada por nome e a unica leitura que esta tabela tem; o indice
  // existe para ela, e so.
  //
  // Sem indice sobre `funcao` ou `ativo`: tres e dois valores distintos, numa
  // tabela de dezenas de linhas, nao pagam o indice.
  //
  // Sem indice UNICO, e isso e decisao: a spec nao pede nome unico, dois
  // colaboradores homonimos sao plausiveis, e duplicata em indice unico sai
  // como HTTP 500 "Duplicate record detected" (fato medido) -- recusa sem
  // motivo legivel, exatamente o que o D10 manda evitar.
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}
