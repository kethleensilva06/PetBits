// A ficha de tutor de quem esta logado.
//
// O tutor e encontrado pelo $auth.id -- o id que o Xano extrai do token --, e
// nunca por um id vindo do corpo ou da URL. E isso que torna impossivel pedir
// a ficha de outra pessoa: nao ha onde informar de quem.
//
// Uma conta sem ficha (a equipe da clinica, por exemplo) recebe resposta vazia
// em vez de erro: nao e falha, e ausencia.
query "me/tutor" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Devolve a ficha de tutor vinculada a conta autenticada"

  input {
  }

  stack {
    db.get tutor {
      field_name = "id_user"
      field_value = $auth.id
    } as $tutor
  }

  response = $tutor
}
