// Cria um registro em pet
query pet verb=POST {
  api_group = "PetBits"

  input {
    // Tutor do pet
    int id_cliente
  
    // Nome do pet
    text nome filters=trim
  
    // Especie do pet
    text especie filters=trim
  
    // Raca do pet
    text raca? filters=trim
  
    // Data de nascimento
    date data_nascimento?
  
    // Peso em quilos
    decimal peso?
  
    // Observacoes gerais
    text observacoes? filters=trim
  }

  stack {
    db.add pet {
      data = {
        id_cliente     : $input.id_cliente
        nome           : $input.nome
        especie        : $input.especie
        raca           : $input.raca
        data_nascimento: $input.data_nascimento
        peso           : $input.peso
        observacoes    : $input.observacoes
      }
    } as $registro
  }

  response = $registro
}