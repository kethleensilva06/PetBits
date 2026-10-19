// O colaborador altera os proprios dados (change `perfil-do-colaborador`, D3).
//
// So nome e telefone. `funcao`, `email`, `data_entrada` e `ativo` NEM ESTAO no
// `input`: nao existem em `$input`, entao o `pick` nao tem como coloca-los em
// `$dados`. Quem define funcao, e-mail e desligamento e a gerencia, pelo
// `equipe/colaboradores/{id}`.
//
// A ficha e a do e-mail da conta do token (D1), provada de novo com lock
// dentro da transacao. Quando o nome vem, o nome da CONTA muda junto: e dele
// que sai a saudacao do topo, e sem isto o nome antigo voltaria na proxima
// entrada.
query "equipe/meu-perfil" verb=PATCH {
  api_group = "PetBits"
  auth = "user"
  description = "Altera nome e telefone da ficha de colaborador da conta de equipe"

  input {
    text nome? filters=trim
    text telefone? filters=trim
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

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $corpo_cru

    var $dados {
      value = `$input|pick:($corpo_cru|keys)`
    }

    precondition (($dados|count) > 0) {
      error_type = "inputerror"
      error = "Informe ao menos um campo para alterar."
    }

    conditional {
      if (($dados|has:"nome") == true) {
        precondition ((($dados|get:"nome")|trim) != "") {
          error_type = "inputerror"
          error = "O nome nao pode ficar em branco."
        }
      }
    }

    db.get user {
      field_name = "id"
      field_value = $id_conta
      output = ["id", "email"]
    } as $conta

    db.transaction {
      stack {
        db.query colaborador {
          where = $db.colaborador.email == $conta.email
          lock = true
          output = ["id"]
          return = {type: "list"}
        } as $fichas

        precondition (($fichas|count) == 1) {
          error_type = "accessdenied"
          error = "Nao ha uma ficha de colaborador com o seu e-mail. Procure a gerencia."
        }

        var $minha {
          value = $fichas|first
        }

        db.patch colaborador {
          field_name = "id"
          field_value = $minha.id
          data = $dados
        } as $atualizada

        conditional {
          if (($dados|has:"nome") == true) {
            db.edit user {
              field_name = "id"
              field_value = $conta.id
              data = {name: $dados|get:"nome"}
            } as $conta_editada
          }
        }
      }
    }
  }

  response = {
    id          : $atualizada.id
    nome        : $atualizada.nome
    funcao      : $atualizada.funcao
    telefone    : $atualizada.telefone
    email       : $atualizada.email
    data_entrada: $atualizada.data_entrada
    foto        : $atualizada.foto
  }
}
