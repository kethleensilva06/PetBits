table "agendamento" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

    int id_pet {
      table = "pet"
      description = "Pet atendido"
    }

    int id_servico {
      table = "servico"
      description = "Servico agendado"
    }

    int id_funcionario {
      table = "funcionario"
      description = "Responsavel pelo atendimento"
    }

    timestamp data_hora {
      description = "Data e hora do agendamento"
    }

    text status filters=trim {
      description = "agendado, em_andamento, concluido ou cancelado"
    }

    text observacoes? filters=trim {
      description = "Observacoes do agendamento"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pet", op: "asc"}]}
    {type: "btree", field: [{name: "id_servico", op: "asc"}]}
    {type: "btree", field: [{name: "id_funcionario", op: "asc"}]}
    {type: "btree", field: [{name: "data_hora", op: "desc"}]}
  ]
}
