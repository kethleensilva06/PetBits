// Substitui os campos de um registro de cliente; envie o registro completo
query "cliente/{id}" verb=PATCH {
  api_group = "PetBits"

  input {
    // Identificador do registro
    int id
  
    // Nome completo do tutor
    text nome? filters=trim
  
    // CPF do tutor
    text cpf? filters=trim
  
    // E-mail de contato
    text email? filters=trim
  
    // Telefone de contato
    text telefone? filters=trim
  
    // Endereco do tutor
    text endereco? filters=trim
  }

  stack {
    db.edit cliente {
      field_name = "id"
      field_value = $input.id
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