// O tutor troca a propria senha (change `perfil-e-fotos`, D5).
//
// A senha atual e conferida AQUI, no servidor: sem isso, quem pegasse um
// celular com a sessao aberta trocaria a senha e tomaria a conta. A nova
// passa pela validacao da coluna `password` da tabela `user`
// (min:8|minAlpha:1|minDigit:1), a mesma do cadastro.
query "me/senha" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Troca a senha da conta autenticada, conferindo a atual"

  input {
    text senha_atual
    text nova_senha
    text confirmar
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    precondition ($input.nova_senha == $input.confirmar) {
      error_type = "inputerror"
      error = "A nova senha e a confirmacao nao conferem."
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $conta

    precondition ($conta != null) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    security.check_password {
      text_password = $input.senha_atual
      hash_password = $conta.password
    } as $atual_confere

    precondition ($atual_confere == true) {
      error_type = "inputerror"
      error = "A senha atual nao confere."
    }

    db.edit user {
      field_name = "id"
      field_value = $conta.id
      data = {password: $input.nova_senha}
    } as $editada

    function.run "Quick Start/log_event" {
      input = {
        user_id : $conta.id
        action  : "senha_trocada"
        metadata: {}
      }
    } as $registrado
  }

  response = {ok: true}
}
