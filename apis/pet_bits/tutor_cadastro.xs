// Cadastro publico do tutor: cria a conta de acesso e a ficha, ja vinculadas.
//
// Nao usamos o auth/signup do template porque ele cria apenas a conta, e a
// especificacao exige que uma recusa nao deixe conta orfa.
//
// A ORDEM IMPORTA (design.md, D4): os dois documentos sao conferidos ANTES de
// qualquer gravacao. Invertido -- criar a conta e so entao checar o documento
// -- uma recusa por documento duplicado deixaria para tras um login sem ficha,
// que e exatamente o cenario "recusa nao deixa conta orfa".
query "tutor/cadastro" verb=POST {
  api_group = "PetBits"
  description = "Cria user (papel member) + tutor vinculado e devolve o authToken"

  input {
    text nome filters=trim
    email email filters=trim|lower
    // A coluna password da tabela user ja valida min:8|minAlpha:1|minDigit:1
    text password
    text documento filters=trim
    text telefone? filters=trim
    text endereco? filters=trim
  }

  stack {
    db.has user {
      field_name = "email"
      field_value = $input.email
    } as $email_existe

    precondition ($email_existe == false) {
      error_type = "accessdenied"
      error = "Ja existe uma conta com este e-mail."
    }

    db.has tutor {
      field_name = "documento"
      field_value = $input.documento
    } as $documento_existe

    // Nao vinculamos automaticamente a uma ficha existente: quem soubesse o
    // documento de outra pessoa passaria a ver os animais e o historico dela.
    // O vinculo de um tutor de balcao e feito pela clinica.
    precondition ($documento_existe == false) {
      error_type = "inputerror"
      error = "Ja existe um cadastro com este documento. Procure a clinica para liberar o seu acesso."
    }

    // O papel e fixado aqui, no servidor. Nenhum valor vindo do corpo da
    // requisicao participa desta decisao.
    db.add user {
      data = {
        created_at: "now"
        name      : $input.nome
        email     : $input.email
        password  : $input.password
        role      : "member"
      }
    } as $user

    db.add tutor {
      data = {
        created_at: "now"
        nome      : $input.nome
        documento : $input.documento
        email     : $input.email
        telefone  : $input.telefone
        endereco  : $input.endereco
        id_user   : $user.id
      }
    } as $tutor

    // Mesmo formato de token do auth/login do template: 24h, sem extras. O
    // papel fica fora do token de proposito -- dentro dele congelaria por 24
    // horas, e rebaixar alguem nao teria efeito ate o token vencer.
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {authToken: $authToken, user_id: $user.id, tutor_id: $tutor.id}
}
