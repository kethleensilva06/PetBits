table agendamento {
  auth = false

  schema {
    // Identificador do registro
    int id
  
    // Pet atendido
    int id_pet {
      table = ""
    }
  
    // Servico agendado
    int id_servico {
      table = ""
    }
  
    // Responsavel pelo atendimento
    int id_funcionario {
      table = ""
    }
  
    // Data e hora do agendamento
    timestamp data_hora
  
    // agendado, em_andamento, concluido ou cancelado
    text status filters=trim
  
    // Observacoes do agendamento
    text observacoes? filters=trim
  
    // Criado automaticamente pelo Xano
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pet", op: "asc"}]}
    {type: "btree", field: [{name: "id_servico", op: "asc"}]}
    {type: "btree", field: [{name: "id_funcionario", op: "asc"}]}
    {type: "btree", field: [{name: "data_hora", op: "desc"}]}
  ]
}