// A pessoa responsavel por um ou mais animais atendidos pela clinica.
//
// O vinculo com a conta de acesso mora aqui, e nao na tabela `user`: daquela
// tabela dependem o login, a troca de senha e os event logs do template, e um
// push errado ali derruba a entrada de todo mundo (design.md, D2).
//
// `id_user` e opcional de proposito: a clinica precisa cadastrar quem chega no
// balcao e nunca vai usar o site. Por isso o indice sobre ele NAO e unico --
// se o Xano gravar um padrao do tipo no lugar de nulo, o segundo tutor sem
// conta estouraria um indice unico. A regra "no maximo um tutor por conta" e
// garantida pelo endpoint de cadastro (design.md, D3).
table tutor {
  auth = false

  schema {
    int id

    // Nome completo do tutor
    text nome filters=trim

    // Documento de identificacao. Unico: duas fichas para a mesma pessoa
    // quebram o historico do animal.
    text documento filters=trim

    // Contato -- opcional, porque nem todo cadastro de balcao tem
    text telefone? filters=trim
    email? email filters=trim|lower
    text endereco? filters=trim

    // Conta de acesso vinculada, quando houver
    int id_user? {
      table = "user"
    }

    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "documento", op: "asc"}]}
    {type: "btree", field: [{name: "id_user", op: "asc"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}
