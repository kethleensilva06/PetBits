table servico {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Nome do servico
    text nome_servico filters=trim
  
    // Descricao do servico
    text descricao? filters=trim
  
    // Preco do servico
    decimal preco filters=min:0
  
    // Duracao estimada em minutos
    int duracao_estimada? filters=min:0
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "nome_servico", op: "asc"}]}
  ]
}