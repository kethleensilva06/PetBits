// Um animal do tutor autenticado, pelo identificador.
//
// Mesmo padrao de leitura da listagem (design.md, D1), com o identificador
// entrando no `where` em vez de num `db.get` -- que nao aceita `where` nem
// `join`, medido no parser.
//
// "Nao existe" e "nao e seu" saem IGUAIS (D6): mesma mensagem, mesmo corpo.
// Identificadores sao sequenciais, e respostas distinguiveis devolveriam o mapa
// de quais animais existem. Numa clinica veterinaria, existencia de registro e
// dado de saude por inferencia. A distincao util para diagnostico vai para o
// registro do servidor, nao para a resposta.
query "pet/{pet_id}" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Devolve um animal do tutor autenticado, ou nao encontrado"

  input {
    int pet_id filters=min:1
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    db.query pet {
      join = {
        tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
      }

      where = ($db.pet.id == $input.pet_id) && ($db.tutor.id_user == $auth.id)
      output = ["id", "nome", "especie", "raca", "data_nascimento", "peso", "observacoes"]
      return = {type: "single"}
    } as $meu

    precondition ($meu != null) {
      error_type = "notfound"
      error = "Animal nao encontrado."
    }
  }

  response = $meu
}
