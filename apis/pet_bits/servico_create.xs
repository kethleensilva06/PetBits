// Cria um registro em servico
query servico verb=POST {
  api_group = "PetBits"

  input {
    // Nome do servico
    text nome_servico filters=trim
  
    // Descricao do servico
    text descricao? filters=trim
  
    // Preco do servico
    decimal preco
  
    // Duracao estimada em minutos
    int duracao_estimada?
  }

  stack {
    db.add servico {
      data = {
        nome_servico    : $input.nome_servico
        descricao       : $input.descricao
        preco           : $input.preco
        duracao_estimada: $input.duracao_estimada
      }
    } as $registro
  }

  response = $registro
}