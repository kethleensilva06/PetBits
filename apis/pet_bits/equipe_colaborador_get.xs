// Um colaborador da clinica, pelo identificador.
//
// Mesma abertura obrigatoria da listagem (design.md, D2): precondition de
// sessao, prova de equipe, e so entao qualquer db.*. Nada e lido antes de o
// direito de ler estar estabelecido.
//
// O identificador entra no `where` da consulta, e nao num `db.get`, que recusa
// `where` e `join` (fato medido 4 do design) -- a mesma forma de `pet_get.xs`,
// e a mesma forma da listagem aqui ao lado, para que o `output` seja explicito
// nos dois e um nao possa divergir do outro sem se notar.
//
// Identificador que nao existe sai como NOTFOUND, nunca como lista vazia nem
// como 200 com corpo nulo: `return = {type: "single"}` devolve nulo quando nada
// casa, e devolver esse nulo seria a tela da equipe mostrando um formulario em
// branco como se fosse um colaborador real.
//
// Aqui "nao existe" NAO precisa ser indistinguivel de "nao e seu", como em
// `pet_get.xs`: colaborador nao tem dono, e quem passou pela prova de equipe ja
// recebe a lista inteira pelo endpoint ao lado. Nao ha o que um identificador
// sondado revele que a listagem ja nao entregue.
query "equipe/colaboradores/{colaborador_id}" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Devolve um colaborador da clinica, ou nao encontrado"

  input {
    int colaborador_id filters=min:1
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    // Simetria de forma, nao seguranca (design.md, D2): a funcao lanca antes de
    // devolver qualquer coisa.
    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    db.query colaborador {
      where = $db.colaborador.id == $input.colaborador_id
      output = ["id", "nome", "funcao", "telefone", "email", "data_entrada", "ativo"]
      return = {type: "single"}
    } as $colaborador

    precondition ($colaborador != null) {
      error_type = "notfound"
      error = "Colaborador nao encontrado."
    }
  }

  response = $colaborador
}
