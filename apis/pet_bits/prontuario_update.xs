// Substitui os campos de um registro de prontuario; envie o registro completo
query "prontuario/{id}" verb=PATCH {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  
    // Pet atendido
    int id_pet?
  
    // Responsavel pelo atendimento
    int id_funcionario?
  
    // Diagnostico registrado
    text diagnostico? filters=trim
  
    // Tratamento realizado
    text tratamento_realizado? filters=trim
  
    // Data da proxima consulta
    date proxima_consulta?
  }

  stack {
    db.edit prontuario {
      field_name = "id"
      field_value = $input.id
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