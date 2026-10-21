// A equipe altera os dados de um tutor (change `editar-tutor`).
//
// EQUIPE, nao gerencia (D1): corrigir o cadastro de quem e atendido e trabalho
// do atendente, como o cadastro de balcao em `equipe_tutor_create.xs`.
//
// So os campos enviados mudam (D2): o padrao `pick` sobre o corpo cru, de
// `equipe_colaborador_update.xs`.
//
// O e-mail da ficha e o de entrada andam juntos (D4): no cadastro pelo site o
// mesmo e-mail vai para `user` e para `tutor`, e o perfil do cliente mostra o
// da ficha. Com conta ligada (`id_user` > 0), mudar um muda o outro, na mesma
// transacao. A senha nao muda (D6).
//
// Conta da equipe nao muda por aqui (D5): se a conta ligada a ficha nao for de
// cliente (`role` == "member", por igualdade), o e-mail e recusado.
query "equipe/tutores/{tutor_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"
  description = "Altera nome, CPF, telefone, e-mail e endereco de um tutor"

  input {
    int tutor_id filters=min:1
    text nome? filters=trim
    text documento? filters=trim
    text telefone? filters=trim
    email email? filters=trim|lower
    text endereco? filters=trim
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
      value = `$input|pick:($corpo_cru|keys)`|unset:"tutor_id"
    }

    precondition (($dados|count) > 0) {
      error_type = "inputerror"
      error = "Informe ao menos um campo para alterar."
    }

    conditional {
      if (($dados|has:"nome") == true) {
        precondition ((($dados|get:"nome")|trim) != "") {
          error_type = "inputerror"
          error = "O nome do tutor nao pode ficar em branco."
        }
      }
    }

    // `db.patch` recusa `where` (fato medido): a existencia e o vinculo vem de
    // uma consulta propria.
    db.query tutor {
      where = $db.tutor.id == $input.tutor_id
      output = ["id", "id_user"]
      return = {type: "single"}
    } as $ficha

    precondition ($ficha != null) {
      error_type = "notfound"
      error = "Tutor nao encontrado."
    }

    // D3: as regras do cadastro. Normalizado, porque `123.456.789-01` e
    // `12345678901` sao o mesmo documento.
    conditional {
      if (($dados|has:"documento") == true) {
        var $documento {
          value = ($dados|get:"documento")|replace:".":""|replace:"-":""|replace:"/":""|replace:" ":""
        }

        precondition (($documento|strlen) == 11) {
          error_type = "inputerror"
          error = "O documento precisa ter 11 digitos."
        }

        function.run "PetBits/cpf_valido" {
          input = {documento: $documento}
        } as $cpf_ok

        precondition ($cpf_ok == true) {
          error_type = "inputerror"
          error = "CPF invalido. Confira os numeros."
        }

        // O proprio tutor pode repetir o CPF que ja tem; outro, nao.
        db.query tutor {
          where = ($db.tutor.documento == $documento) && ($db.tutor.id != $ficha.id)
          return = {type: "count"}
        } as $outros_com_documento

        precondition ($outros_com_documento == 0) {
          error_type = "inputerror"
          error = "Este documento ja esta cadastrado para outro tutor."
        }

        var.update $dados {
          value = $dados|set:"documento":$documento
        }
      }
    }

    var $muda_email_da_conta {
      value = false
    }

    // D4 e D5: o e-mail nao pode ser de outro tutor nem de outra conta; com
    // conta ligada, ela tem de ser de cliente e nao fica sem e-mail.
    conditional {
      if (($dados|has:"email") == true) {
        var $email {
          value = $dados|get:"email"
        }

        conditional {
          if ($ficha.id_user > 0) {
            precondition ($email != "") {
              error_type = "inputerror"
              error = "Este tutor tem conta no site: o e-mail nao pode ficar em branco."
            }

            db.get user {
              field_name = "id"
              field_value = $ficha.id_user
              output = ["id", "role"]
            } as $conta_do_tutor

            precondition ($conta_do_tutor != null) {
              error_type = "inputerror"
              error = "A conta ligada a este tutor nao foi encontrada."
            }

            precondition ($conta_do_tutor.role == "member") {
              error_type = "accessdenied"
              error = "Esta ficha esta ligada a uma conta da equipe; o e-mail dela nao muda por aqui."
            }

            var.update $muda_email_da_conta {
              value = true
            }
          }
        }

        conditional {
          if ($email != "") {
            db.query tutor {
              where = ($db.tutor.email == $email) && ($db.tutor.id != $ficha.id)
              return = {type: "count"}
            } as $outros_tutores_com_email

            precondition ($outros_tutores_com_email == 0) {
              error_type = "inputerror"
              error = "Este e-mail ja esta em uso por outro tutor."
            }

            db.query user {
              where = ($db.user.email == $email) && ($db.user.id != $ficha.id_user)
              return = {type: "count"}
            } as $outras_contas_com_email

            precondition ($outras_contas_com_email == 0) {
              error_type = "inputerror"
              error = "Este e-mail ja esta em uso por outra conta."
            }
          }
        }
      }
    }

    // A ficha e a conta mudam juntas, ou nenhuma muda (D4).
    db.transaction {
      stack {
        db.patch tutor {
          field_name = "id"
          field_value = $ficha.id
          data = $dados
        } as $atualizada

        conditional {
          if ($muda_email_da_conta == true) {
            db.edit user {
              field_name = "id"
              field_value = $ficha.id_user
              data = {email: $dados|get:"email"}
            } as $conta_editada
          }
        }
      }
    }
  }

  response = {
    id       : $atualizada.id
    nome     : $atualizada.nome
    documento: $atualizada.documento
    telefone : $atualizada.telefone
    email    : $atualizada.email
    endereco : $atualizada.endereco
  }
}
