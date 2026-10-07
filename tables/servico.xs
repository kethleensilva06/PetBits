// O que a clinica oferece, com preco e duracao estimada.
//
// A duracao e o que torna a agenda calculavel: sem ela nao ha como saber se
// dois atendimentos se sobrepoem (spec de servicos). Por isso ela e
// obrigatoria e tem de ser maior que zero -- e a segunda metade dessa frase
// esta FORA desta declaracao, ver abaixo.
//
// Como em `colaborador`, nenhuma coluna aponta para `user` ou para `tutor`
// (design.md, D2): o catalogo e da clinica, nao de uma conta. Nao existe
// `where` de posse nesta tabela, e a unica recusa e a chamada a
// `PetBits/exige_equipe` como segunda instrucao de todo endpoint que a toca.
table servico {
  auth = false

  schema {
    int id

    // Nome do servico, como ele aparece no catalogo
    text nome filters=trim

    // Opcional: a spec tem cenario proprio de servico criado sem descricao
    text descricao? filters=trim

    // Os dois sao obrigatorios -- mas obrigatorio AQUI e declaracao de
    // intencao, nao barreira. Foi medido que o Xano grava 0 no lugar de um
    // vinculo omitido, e nao ha motivo para um numero omitido chegar
    // diferente: 0 satisfaz um decimal e um int obrigatorios, e passaria.
    //
    // Quem recusa de verdade sao as precondition antes do db.add e do
    // db.patch, na criacao E na alteracao (design.md, D10): duracao > 0 e
    // preco >= 0. A assimetria entre as duas e proposital -- preco 0 tem de
    // PASSAR, porque servico gratuito e valido pela spec; duracao 0 nao, e o
    // `pick` do PATCH torna possivel zera-la numa alteracao, que e o cenario
    // que a spec cobra por nome.
    decimal preco
    int duracao_minutos

    timestamp created_at?=now
  }

  // O catalogo e lido inteiro e ordenado por nome; e a unica leitura que esta
  // tabela tem, e o indice existe para ela.
  //
  // Sem indice UNICO sobre `nome`, embora dois servicos "Banho" sejam
  // claramente erro de digitacao: a spec nao pede unicidade, e duplicata em
  // indice unico sai como HTTP 500 "Duplicate record detected" (fato medido),
  // nao como recusa com motivo. Se um dia o catalogo precisar de nome unico,
  // o lugar e uma precondition com mensagem, no padrao do D10 -- nao aqui.
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}
