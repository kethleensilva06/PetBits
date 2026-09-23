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
  
    // Momento do cadastro
    timestamp data_cadastro?=now
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "cpf", op: "asc"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}