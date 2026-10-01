// O animal sob cuidado da clinica. E o sujeito do historico clinico: consultas,
// agendamentos e atendimentos sao dele, nao do tutor.
//
// `id_tutor` e obrigatorio -- mas isso e declaracao de intencao, nao barreira.
// Foi medido que o Xano grava 0, e nao nulo, num vinculo omitido, e 0 satisfaz
// um inteiro obrigatorio (design.md, D3). Quem impede o orfao e a precondition
// antes do db.add; quem o esconde, caso apareca, e o inner join ate tutor.
//
// NENHUMA coluna leva indice unico, e isso e decisao, nao esquecimento
// (design.md, D8): duplicata estoura com erro do motor ABAIXO do `where` de
// posse, entao um indice unico em microchip -- candidato obvio para quem
// mexer nesta tabela depois -- viraria oraculo de existencia, confirmando que
// um animal e cliente da clinica sem nunca le-lo.
table pet {
  auth = false

  schema {
    int id

    // Tutor responsavel. O valor vem sempre do token, nunca da requisicao.
    int id_tutor {
      table = "tutor"
    }

    // Nome do animal
    text nome filters=trim

    // Cao, gato, ave...
    text especie filters=trim

    // Raca, quando conhecida
    text raca? filters=trim

    // `timestamp`, e nao `date`, por limitacao medida do Xano: um input
    // declarado a mao com tipo `date` derruba o endpoint com 500 "Unable to
    // locate input" quando o campo e OMITIDO, mesmo declarado opcional e
    // mesmo com valor padrao. `timestamp` tolera a ausencia (chega como 0).
    timestamp data_nascimento?

    decimal peso?

    // Alergias, cuidados especiais -- dado clinico. Uma edicao nao pode
    // apaga-lo por omissao (design.md, D8).
    text observacoes? filters=trim

    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_tutor", op: "asc"}]}
    {type: "btree", field: [{name: "id_tutor", op: "asc"}, {name: "nome", op: "asc"}]}
  ]
}
