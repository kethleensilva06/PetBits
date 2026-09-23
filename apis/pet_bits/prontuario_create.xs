// Cria um registro em prontuario
query prontuario verb=POST {
  api_group = "PetBits"

  input {
    // Pet atendido
    int id_pet
  
    // Responsavel pelo atendimento
    int id_funcionario
  
    // Diagnostico registrado
    text diagnostico? filters=trim
  
    // Tratamento realizado
    text tratamento_realizado? filters=trim
  
    // Data da proxima consulta
    date proxima_consulta?
  }

  stack {
    db.add prontuario {
      data = {
        id_pet              : $input.id_pet
        id_funcionario      : $input.id_funcionario
        diagnostico         : $input.diagnostico
        tratamento_realizado: $input.tratamento_realizado
        proxima_consulta    : $input.proxima_consulta
      }
    } as $registro
  }

  response = $registro
}