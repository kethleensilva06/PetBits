table cliente {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Nome completo do tutor
    text nome filters=trim
  
    // CPF do tutor
    text cpf filters=trim
  
    // E-mail de contato
    text email? filters=trim
  
    // Telefone de contato
    text telefone? filters=trim
  
    // Endereco do tutor
    text endereco? filters=trim

    // Login associado a este tutor. Fica vazio quando o cadastro foi feito no
    // balcao e o tutor ainda nao tem acesso ao aplicativo. E por este campo que
    // se descobre "quais pets sao do usuario logado".
    int id_user? {
      table = "user"
    }

    // Momento do cadastro
    timestamp data_cadastro?=now
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  // O indice de id_user nao e unique de proposito: o Xano grava 0 no lugar de
  // null nas escritas via dblink, e o segundo tutor de balcao (sem login)
  // estouraria um indice unico. A regra "um tutor por login" fica na aplicacao.
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "cpf", op: "asc"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
    {type: "btree", field: [{name: "id_user", op: "asc"}]}
  ]
}