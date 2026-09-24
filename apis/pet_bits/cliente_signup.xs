// Cadastro publico do tutor: cria o login e a ficha de cliente ja vinculados
query "cliente/signup" verb=POST {
  api_group = "PetBits"
  description = "Cria user (role member) + cliente vinculado e devolve o authToken"

  input {
    text nome filters=trim
    email email filters=trim|lower
    // A coluna password da tabela user ja valida min:8|minAlpha:1|minDigit:1
    text password
    text cpf filters=trim
    text telefone? filters=trim
    text endereco? filters=trim
  }

  stack {
    // Mesma regra do auth/signup do template: e-mail e unico na tabela user.
    db.has user {
      field_name = "email"
      field_value = $input.email
    } as $email_existe

    precondition ($email_existe == false) {
      error_type = "accessdenied"
      error = "Este e-mail ja esta em uso."
    }

    // O cpf tem indice unico em cliente. Checar antes evita criar um user que
    // ficaria orfao quando o db.add cliente falhasse logo em seguida.
    db.has cliente {
      field_name = "cpf"
      field_value = $input.cpf
    } as $cpf_existe

    // Nao vinculamos automaticamente a uma ficha existente: quem soubesse o
    // CPF de outra pessoa passaria a ver os pets e os prontuarios dela. O
    // vinculo de um tutor de balcao e feito pela clinica.
    precondition ($cpf_existe == false) {
      error_type = "inputerror"
      error = "Ja existe um cadastro com este CPF. Procure a clinica para liberar o seu acesso."
    }

    // O tipo password da coluna faz o hash sozinho.
    db.add user {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        name      : $input.nome
        email     : $input.email
        password  : $input.password
        role      : "member"
      }
    } as $user

    db.add cliente {
      enforce_hidden_fields = false
      data = {
        created_at   : "now"
        data_cadastro: "now"
        nome         : $input.nome
        cpf          : $input.cpf
        email        : $input.email
        telefone     : $input.telefone
        endereco     : $input.endereco
        id_user      : $user.id
      }
    } as $cliente

    // Mesmo formato de token do auth/login: 24h, sem extras.
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {authToken: $authToken, user_id: $user.id, cliente_id: $cliente.id}
}
