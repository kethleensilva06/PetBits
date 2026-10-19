// A ficha de colaborador de quem esta logado (change `perfil-do-colaborador`).
//
// Colaborador e registro, nao credencial: a ficha nao tem vinculo com conta.
// A ligacao e pelo E-MAIL DA CONTA do token (design.md, D1) -- o e-mail da
// ficha e mantido pela gerencia, entao e ela quem decide de quem e cada ficha.
// Nada vem do corpo nem da URL: nao ha onde informar de quem.
//
// Conta de equipe sem ficha com o mesmo e-mail recebe `ficha: null`, e nao
// erro: e ausencia, e a tela mostra o aviso. Duas fichas com o mesmo e-mail
// sao ambiguas e recusam, em vez de escolher uma.
query "equipe/meu-perfil" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Devolve a ficha de colaborador ligada a conta de equipe pelo e-mail"

  input {
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

    db.get user {
      field_name = "id"
      field_value = $id_conta
      output = ["id", "name", "email"]
    } as $conta

    db.query colaborador {
      where = $db.colaborador.email == $conta.email
      output = ["id", "nome", "funcao", "telefone", "email", "data_entrada", "ativo", "foto"]
      return = {type: "list"}
    } as $fichas

    precondition (($fichas|count) <= 1) {
      error_type = "inputerror"
      error = "Ha mais de uma ficha com o seu e-mail. Procure a gerencia."
    }

    var $ficha {
      value = null
    }

    conditional {
      if (($fichas|count) == 1) {
        var.update $ficha {
          value = $fichas|first
        }
      }
    }
  }

  response = {conta: {nome: $conta.name, email: $conta.email}, ficha: $ficha}
}
