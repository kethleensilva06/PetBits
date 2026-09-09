query "agendamento/{id}" verb=PATCH {
  api_group = "petbits"
  description = "Substitui os campos de um registro de agendamento; envie o registro completo"
  input {
    int id {
      description = "Identificador do registro"
    }

    int id_pet? {
      description = "Pet atendido"
    }

    int id_servico? {
      description = "Servico agendado"
    }

    int id_funcionario? {
      description = "Responsavel pelo atendimento"
    }

    timestamp data_hora? {
      description = "Data e hora do agendamento"
    }

    text status? filters=trim {
      description = "agendado, em_andamento, concluido ou cancelado"
    }

    text observacoes? filters=trim {
      description = "Observacoes do agendamento"
    }
  }
  stack {
    db.edit "agendamento" {
      field_name = "id"
      field_value = $input.id
      data = {
        id_pet: $input.id_pet,
        id_servico: $input.id_servico,
        id_funcionario: $input.id_funcionario,
        data_hora: $input.data_hora,
        status: $input.status,
        observacoes: $input.observacoes
      }
    } as $registro
  }
  response = $registro
}
