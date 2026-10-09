// Stores user information and allows the user to authenticate  against
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1
  
    // The role of the user within their company (e.g., 'admin', 'member').
    //
    // `staff` foi criado no painel do Xano, fora do repositorio; este arquivo
    // so registra o que o `workspace pull` mostrou (change `papel-staff`, D2).
    // `admin` e `staff` sao papeis de equipe; `member` e tutor.
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