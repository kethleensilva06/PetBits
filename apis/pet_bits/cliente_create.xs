// Cria um registro em cliente
query cliente verb=POST {
  api_group = "PetBits"

  input {
    // Nome completo do tutor
    text nome filters=trim
  
    // CPF do tutor
    text cpf filters=trim
  
    // E-mail de contato
    text email? filters=trim
  
    // Telefone de contato
    text telefone? filters=trim
  
    // Endereco do tutor
    text endereco? filters=trim
  }

  stack {
    db.add cliente {
      data = {
        nome    : $input.nome
        cpf     : $input.cpf
        email   : $input.email
        telefone: $input.telefone
        endereco: $input.endereco
      }
    } as $registro
  }

  response = $registro
}