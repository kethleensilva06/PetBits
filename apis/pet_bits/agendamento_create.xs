// Cria um registro em agendamento
query agendamento verb=POST {
  api_group = "PetBits"

  input {
    // Pet atendido
    int id_pet
  
    // Servico agendado
    int id_servico
  
    // Responsavel pelo atendimento
    int id_funcionario
  
    // Data e hora do agendamento
    timestamp data_hora
  
    // agendado, em_andamento, concluido ou cancelado
    text status filters=trim
  
    // Observacoes do agendamento
    text observacoes? filters=trim
  }

  stack {
    db.add agendamento {
      data = {
        id_pet        : $input.id_pet
        id_servico    : $input.id_servico
        id_funcionario: $input.id_funcionario
        data_hora     : $input.data_hora
        status        : $input.status
        observacoes   : $input.observacoes
      }
    } as $registro
  }

  response = $registro
}