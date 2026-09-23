// Substitui os campos de um registro de funcionario; envie o registro completo
query "funcionario/{id}" verb=PATCH {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  
    // Nome do colaborador
    text nome? filters=trim
  
    // CPF do colaborador
    text cpf? filters=trim
  
    // veterinario, tosador ou atendente
    text cargo? filters=trim
  
    // Telefone de contato
    text telefone? filters=trim
  
    // E-mail de contato
    text email? filters=trim
  
    // Data de contratacao
    date data_contratacao?
  }

  stack {
    db.edit funcionario {
      field_name = "id"
      field_value = $input.id
      data = {
        nome            : $input.nome
        cpf             : $input.cpf
        cargo           : $input.cargo
        telefone        : $input.telefone
        email           : $input.email
        data_contratacao: $input.data_contratacao
      }
    } as $registro
  }

  response = $registro
}