query "agendamento" verb=POST {
  api_group = "PetBits"
  description = "Cria um registro em agendamento"
  input {
    int id_pet {
      description = "Pet atendido"
    }

    int id_servico {
      description = "Servico agendado"
    }

    int id_funcionario {
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
  }
  stack {
    db.add "agendamento" {
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
