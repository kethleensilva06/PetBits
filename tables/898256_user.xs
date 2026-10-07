// Stores user information and allows the user to authenticate  against
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1
  
    // O papel decide o ALCANCE da conta, e nada mais o decide: nem o token
    // (que nao o carrega de proposito), nem o cargo na ficha de colaborador
    // (que nao liga a conta nenhuma), nem o cliente.
    //
    //   admin   gerencia da clinica -- alcanca tudo, inclusive manter o quadro
    //   staff   equipe comum -- alcanca a clinica, NAO mantem o quadro
    //   member  tutor -- so os proprios animais
    //
    // A coluna e OPCIONAL, e isso nao e descuido do template: conta nasce a
    // mao no painel, e esquecer o papel e o erro de operacao mais provavel do
    // projeto. Por isso toda conferencia e por IGUALDADE contra os valores
    // esperados -- vazio, erro de digitacao e valor futuro caem todos do lado
    // negado.
    enum role? {
      values = ["admin", "staff", "member"]
    }
  
    object password_reset? {
      schema {
        password token?
        timestamp? expiration?
        bool used?
      }
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
}