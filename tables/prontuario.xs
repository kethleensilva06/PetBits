table "prontuario" {
  auth = false
  schema {
    int id {
      description = "Identificador do registro"
    }

    int id_pet {
      table = "pet"
      description = "Pet atendido"
    }

    int id_funcionario {
      table = "funcionario"
      description = "Responsavel pelo atendimento"
    }

    text diagnostico? filters=trim {
      description = "Diagnostico registrado"
    }

    text tratamento_realizado? filters=trim {
      description = "Tratamento realizado"
    }

    date proxima_consulta? {
      description = "Data da proxima consulta"
    }

    timestamp data_atendimento?=now {
      description = "Momento do atendimento"
    }

    timestamp created_at?=now {
      description = "Criado automaticamente pelo Xano"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pet", op: "asc"}]}
    {type: "btree", field: [{name: "id_funcionario", op: "asc"}]}
    {type: "btree", field: [{name: "data_atendimento", op: "desc"}]}
  ]
}
