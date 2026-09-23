table funcionario {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Nome do colaborador
    text nome filters=trim
  
    // CPF do colaborador
    text cpf filters=trim
  
    // veterinario, tosador ou atendente
    text cargo filters=trim
  
    // Telefone de contato
    text telefone? filters=trim
  
    // E-mail de contato
    text email? filters=trim
  
    // Data de contratacao
    date data_contratacao?
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "cpf", op: "asc"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}