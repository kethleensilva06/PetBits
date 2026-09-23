// Cria um registro em funcionario
query funcionario verb=POST {
  api_group = "PetBits"

  input {
    // Nome do colaborador
    text nome filters=trim
  
    // CPF do colaborador
    text cpf filters=trim
  
    // veterinario, tosador ou atendente
    text cargo filters=trim
  
    // Telefone de contato
    text telefone? filters=trim
  
    // E-mail de contato
    text email? filters=trim
  
    // Data de contratacao
    date data_contratacao?
  }

  stack {
    db.add funcionario {
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