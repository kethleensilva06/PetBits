table pet {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Tutor do pet
    int id_cliente {
      table = "cliente"
    }
  
    // Nome do pet
    text nome filters=trim
  
    // Especie do pet
    text especie filters=trim
  
    // Raca do pet
    text raca? filters=trim
  
    // Data de nascimento
    date data_nascimento?
  
    // Peso em quilos
    decimal peso? filters=min:0
  
    // Observacoes gerais
    text observacoes? filters=trim
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_cliente", op: "asc"}]}
    {type: "btree", field: [{name: "nome", op: "asc"}]}
  ]
}