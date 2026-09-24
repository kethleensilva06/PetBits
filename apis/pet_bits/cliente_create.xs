// Cria um registro em cliente
query cliente verb=POST {
  api_group = "PetBits"

  // id_user liga a ficha a um login. O dblink espelha o schema inteiro, entao
  // sem o override abaixo qualquer requisicao poderia reapontar uma ficha para
  // outro login e, com isso, herdar os pets, os prontuarios e os pedidos
  // daquele tutor. Quem grava id_user e so o cliente/signup, com o id que o
  // proprio servidor acabou de criar.
  input {
    dblink {
      table = "cliente"
      override = {
        id_user: {hidden: true}
      }
    }
  }

  stack {
    db.add cliente {
      enforce_hidden_fields = false
      data = {created_at: "now", data_cadastro: "now"}
    } as $registro
  }

  response = $registro
}