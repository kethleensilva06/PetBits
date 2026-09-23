table prontuario {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Pet atendido
    int id_pet {
      table = "pet"
    }
  
    // Responsavel pelo atendimento
    int id_funcionario {
      table = "funcionario"
    }
  
    // Diagnostico registrado
    text diagnostico? filters=trim
  
    // Tratamento realizado
    text tratamento_realizado? filters=trim
  
    // Data da proxima consulta
    date proxima_consulta?
  
    // Momento do atendimento
    timestamp data_atendimento?=now
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pet", op: "asc"}]}
    {type: "btree", field: [{name: "id_funcionario", op: "asc"}]}
    {
      type : "btree"
      field: [{name: "data_atendimento", op: "desc"}]
    }
  ]
}