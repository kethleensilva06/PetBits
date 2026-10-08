// Cria a ficha de tutor da PROPRIA conta, quando ela ainda nao tem uma.
//
// Existe para o funcionario que tambem e cliente (change
// `cadastro-de-cliente-pela-conta`): a conta de equipe ja existe, mas a ficha
// de tutor so nascia junto com a conta, no cadastro publico.
//
// O dono e o token (D1), no padrao do `pet_create.xs`: nao ha `id_user` na
// entrada, e nome e e-mail vem da propria conta. Nada que o cliente mande
// escolhe de quem e a ficha.
//
// O documento segue o `tutor_cadastro.xs` linha por linha (D3) -- mesma
// normalizacao, mesmos 11 digitos, mesma unicidade e, sobretudo, a MESMA
// recusa generica quando o CPF ja existe. O endpoint exige login, mas uma
// conta qualquer sondando CPFs descobriria quem e cliente da clinica se a
// recusa dissesse "CPF em uso".
query "me/tutor" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cria a ficha de tutor da conta autenticada, se ela ainda nao tiver"

  input {
    text documento filters=trim
    text telefone? filters=trim
    text endereco? filters=trim
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    var $documento {
      value = $input.documento|replace:".":""|replace:"-":""|replace:"/":""|replace:" ":""
    }

    precondition (($documento|strlen) == 11) {
      error_type = "inputerror"
      error = "O documento precisa ter 11 digitos."
    }

    db.has tutor {
      field_name = "documento"
      field_value = $documento
    } as $documento_existe

    // Motivo no registro, resposta generica (D3, igual ao cadastro publico).
    conditional {
      if ($documento_existe == true) {
        function.run "Quick Start/log_event" {
          input = {
            user_id : $auth.id
            action  : "ficha_propria_recusada"
            metadata: {documento_em_uso: true}
          }
        } as $motivo_registrado
      }
    }

    precondition ($documento_existe == false) {
      error_type = "inputerror"
      error = "Nao foi possivel concluir o cadastro. Procure a clinica."
    }

    // D2: a leitura da conta TRAVA a linha dela. Duas requisicoes
    // simultaneas da mesma conta sao serializadas -- a segunda ja ve a ficha
    // da primeira e e recusada. Duas fichas fariam `tutor_do_token` falhar
    // para sempre nesta conta.
    db.transaction {
      stack {
        db.query user {
          where = $db.user.id == $auth.id
          lock = true
          output = ["id", "name", "email"]
          return = {type: "single"}
        } as $conta

        precondition ($conta != null) {
          error_type = "accessdenied"
          error = "Sessao invalida."
        }

        db.has tutor {
          field_name = "id_user"
          field_value = $conta.id
        } as $ja_tem_ficha

        precondition ($ja_tem_ficha == false) {
          error_type = "inputerror"
          error = "Esta conta ja tem cadastro de cliente."
        }

        db.add tutor {
          data = {
            created_at: "now"
            nome      : $conta.name
            documento : $documento
            email     : $conta.email
            telefone  : $input.telefone
            endereco  : $input.endereco
            id_user   : $conta.id
          }
        } as $tutor
      }
    }
  }

  response = {id: $tutor.id, nome: $tutor.nome}
}
