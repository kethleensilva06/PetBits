//  Cadastro publico do tutor: cria a conta de acesso e a ficha, ja vinculadas.
// 
//  Nao usamos o auth/signup do template porque ele cria apenas a conta, e a
//  especificacao exige que uma recusa nao deixe conta orfa.
// 
//  A ORDEM IMPORTA (design.md, D4): os dois documentos sao conferidos ANTES de
//  qualquer gravacao. Invertido -- criar a conta e so entao checar o documento
//  -- uma recusa por documento duplicado deixaria para tras um login sem ficha,
//  que e exatamente o cenario "recusa nao deixa conta orfa".
// Cria user (papel member) + tutor vinculado e devolve o authToken
query "tutor/cadastro" verb=POST {
  api_group = "PetBits"

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
    // `123.456.789-01` e `12345678901` sao o MESMO documento. Sem normalizar,
    // os dois criam duas fichas para a mesma pessoa -- exatamente o que o
    // indice unico existe para impedir, contornado por pontuacao. O filtro de
    // entrada nao aceita `replace`, entao a normalizacao acontece aqui, e e
    // este valor que vai tanto para a conferencia quanto para a gravacao.
    var $documento {
      value = $input.documento
        |replace:".":""
        |replace:"-":""
        |replace:"/":""
        |replace:" ":""
    }
  
    precondition (($documento|strlen) == 11) {
      error_type = "inputerror"
      error = "O documento precisa ter 11 digitos."
    }
  
    db.has user {
      field_name = "email"
      field_value = $input.email
    } as $email_existe
  
    db.has tutor {
      field_name = "documento"
      field_value = $documento
    } as $documento_existe
  
    //  As duas recusas saem IGUAIS -- mesma mensagem, mesmo error_type, logo
    //  mesmo status. Este endpoint e PUBLICO: distinguir "e-mail em uso" de
    //  "documento em uso" confirmaria, sem token nenhum, se um CPF alvo e
    //  cliente da clinica. Numa clinica veterinaria isso e dado de saude por
    //  inferencia.
    // 
    //  E a mesma decisao que o resto desta change aplica a leitura de animais
    //  (design.md, D6), trazida para o endpoint que antecede tudo: e dele que
    //  nasce todo identificador de tutor em que o sistema depois confia.
    // 
    //  O motivo especifico nao se perde: vai para o event_log, onde serve ao
    //  diagnostico sem servir a quem esta sondando. Diagnostico pelo registro,
    //  privacidade pela resposta.
    conditional {
      if ($email_existe || $documento_existe) {
        function.run "Quick Start/log_event" {
          input = {
            user_id : 0
            action  : "cadastro_recusado"
            metadata: {
            email_em_uso    : $email_existe
            documento_em_uso: $documento_existe
            email           : $input.email
          }
          }
        } as $motivo_registrado
      }
    }
  
    precondition (($email_existe == false) && ($documento_existe == false)) {
      error_type = "inputerror"
      error = "Nao foi possivel concluir o cadastro. Procure a clinica."
    }
  
    // As duas gravacoes vao juntas ou nao vao. Medido na tarefa 2.7: o
    // db.transaction do Xano faz rollback de verdade -- um erro depois do
    // primeiro db.add desfaz o primeiro db.add. Isso torna "recusa nao deixa
    // conta orfa" uma garantia estrutural, e nao so uma questao de ordem.
    db.transaction {
      stack {
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
      
        //  "No maximo um tutor por conta" nao pode ser garantido por indice: a
        //  medicao da tarefa 1.2 mostrou que o Xano grava 0, e nao nulo, quando o
        //  vinculo e omitido -- um indice unico sobre id_user recusaria o segundo
        //  tutor de balcao. Entao a garantia mora aqui.
        // 
        //  Hoje a conta acabou de ser criada e a checagem nunca falha. Ela existe
        //  porque este endpoint e o modelo do qual o vinculo de tutor de balcao
        //  vai ser derivado, e e ali que ela passa a ser necessaria de verdade.
        db.has tutor {
          field_name = "id_user"
          field_value = $user.id
        } as $conta_ja_vinculada
      
        precondition ($conta_ja_vinculada == false) {
          error_type = "accessdenied"
          error = "Esta conta ja esta vinculada a um cadastro de tutor."
        }
      
        db.add tutor {
          data = {
            created_at: "now"
            nome      : $input.nome
            documento : $documento
            email     : $input.email
            telefone  : $input.telefone
            endereco  : $input.endereco
            id_user   : $user.id
          }
        } as $tutor
      }
    }
  
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

  response = {
    authToken: $authToken
    user_id  : $user.id
    tutor_id : $tutor.id
  }

  guid = "sOnvSX9iwP0gbNJvmsRsMCt8SKA"
}