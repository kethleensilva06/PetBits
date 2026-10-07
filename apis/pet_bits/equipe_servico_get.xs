// Um servico do catalogo, pelo identificador.
//
// Mesma abertura da listagem, e pelo mesmo motivo (design.md, D2): sem coluna
// de dono, a funcao e a unica recusa que existe.
//
// ATENCAO A QUEM COPIAR ESTE ARQUIVO: aqui "nao existe" PODE sair como
// "nao encontrado" explicito, e isso nao contradiz o pet_get.xs. La os dois
// casos sao indistinguiveis de proposito porque o identificador e sequencial e
// a existencia de um ANIMAL e dado de saude por inferencia. Aqui quem passou
// pela prova e a propria clinica, e o catalogo e dela: nao ha de quem esconder
// que um servico existe. O que nao pode e virar lista vazia -- "nao encontrado"
// precisa ser recusa, nao um 200 com nada dentro, que a tela leria como
// "o servico foi apagado".
//
// Por que `db.query` com `where` e nao `db.get` pelo id: `db.get` recusa
// `where` e nao foi exercitado neste projeto com `output` explicito, e e o
// `output` que impede coluna nova de vazar (D8). A forma abaixo e a mesma de
// `pet_get.xs`, ja em producao.
query "equipe/servicos/{servico_id}" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Devolve um servico do catalogo da clinica, ou nao encontrado"

  input {
    int servico_id filters=min:1
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // So AQUI, com o direito ja estabelecido, o banco e tocado.
    db.query servico {
      where = $db.servico.id == $input.servico_id
      output = ["id", "nome", "descricao", "preco", "duracao_minutos", "categoria"]
      return = {type: "single"}
    } as $servico

    precondition ($servico != null) {
      error_type = "notfound"
      error = "Servico nao encontrado."
    }
  }

  response = $servico
}
