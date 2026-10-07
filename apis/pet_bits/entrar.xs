// A entrada do PetBits, em tempo constante.
//
// Endpoint PROPRIO, e nao uma edicao do `auth/login` do template: aquele
// arquivo e objeto `xano:quick-start` e um re-push o desfaz (design.md, D3,
// item 6). E o mesmo argumento que ja derrubou a `enforce_role`.
//
// O QUE ESTE ARQUIVO CONSERTA (design.md, D6). O auth/login do template roda
// nesta ordem:
//
//   precondition ($user != null)   <- decide ANTES
//   security.check_password        <- so entao paga o bcrypt
//
// Entao e-mail inexistente responde sem nunca pagar o custo do hash, e e-mail
// existente com senha errada paga. A diferenca e de dezenas de milissegundos,
// e e cronometravel de fora SEM CREDENCIAL NENHUMA -- ou seja, o relogio
// responde "esta conta existe" para quem perguntar. Com as abas Cliente e
// Colaborador na tela, "este e-mail e da clinica?" deixa de ser curiosidade e
// vira o organograma.
//
// A correcao: `security.check_password` roda SEMPRE, na mesma posicao da
// pilha, inclusive quando a conta nao existe -- contra um hash de descarte. A
// decisao so acontece depois, e as duas recusas saem iguais.
//
// O QUE ELE NAO DEVOLVE: o papel. Se o corpo do sucesso trouxesse `role`, a
// aba Colaborador poderia decidir sozinha para onde mandar a pessoa, sem o
// `GET /auth/me`, e o oraculo de papel voltaria inteiro (design.md, D5,
// invariante 4). Pelo mesmo motivo o papel fica fora do token (`extras = {}`):
// dentro dele congelaria por 24 horas, e rebaixar alguem nao teria efeito ate
// o token vencer.
query entrar verb=POST {
  api_group = "PetBits"
  description = "Inicia sessao e devolve authToken; recusa em tempo constante"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    // Hash de descarte. NAO corresponde a conta nenhuma: e o bcrypt de uma
    // senha aleatoria de 32 caracteres, gerada para este arquivo e descartada
    // sem nunca ter sido anotada -- ninguem, inclusive quem escreveu isto,
    // sabe que senha casa com ele.
    //
    // Ele precisa ser um bcrypt SINTATICAMENTE VALIDO, e nao `""`: medido na
    // tarefa 1.3 que `security.check_password` com hash vazio lanca
    // ERROR_FATAL "Invalid password syntax." Um ERROR_FATAL que acontece so no
    // caminho do e-mail inexistente seria o mesmo oraculo de volta, agora
    // gritando o proprio nome no corpo da resposta.
    //
    // O PREFIXO e `$2a$`, e a escolha nao e indiferente. `$2a$` e o unico
    // aceito por TODAS as implementacoes de bcrypt: PHP (`crypt` documenta
    // `$2a$`, `$2x$` e `$2y$` -- e NAO `$2b$`), Go, Python, Node, Java. Se o
    // motor do Xano for PHP e o hash vier com `$2b$`, `crypt` nao calcula
    // nada: devolve falha na hora. E isso nao e um erro visivel -- e um
    // `false` instantaneo, ou seja, o caminho do e-mail inexistente volta a
    // custar quase zero enquanto o da senha errada paga o bcrypt inteiro, e o
    // oraculo de tempo que este arquivo existe para fechar reabre sem que nada
    // na resposta mude. `$2a$` nao levanta a pergunta em motor nenhum.
    //
    // MEDIDO, e custou uma rodada: o Xano NAO usa bcrypt. Um `$2a$10$...`
    // sintaticamente perfeito faz `security.check_password` responder
    // ERROR_FATAL "Invalid password syntax." com HTTP 500 -- ou seja, a
    // primeira versao deste arquivo devolvia 500 para e-mail inexistente e
    // 403 para senha errada, e criava um oraculo MAIS barulhento do que o de
    // tempo que ela vinha fechar. O formato do Xano tem 81 caracteres e e
    // salgado por linha.
    //
    // Por isso o valor abaixo foi GERADO pelo proprio Xano: uma conta
    // temporaria criada com senha aleatoria de 32 caracteres, o hash lido da
    // tabela, e a conta apagada em seguida. A senha nunca foi anotada e nao
    // existe mais em lugar nenhum -- nem quem gerou sabe qual e.
    var $hash_descarte {
      value = "7d99aa01ea02f83b.039ebbfdcb057745a665ecf34bdeb8ceece876e375114ed461255a298076f267"
    }

    // A busca vem antes da conferencia, como no template. A diferenca e que
    // aqui ela nao decide nada.
    //
    // O `output` carrega so o que a pilha usa (design.md, D2): o hash entra
    // porque o check precisa dele, e nao sai deste arquivo em lugar nenhum --
    // nem na resposta, nem no metadata do log. O template pede
    // `["id", "created_at", "name", "email", "password", "role"]` e e dai que
    // nasce o vazamento do D6.
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "email", "password"]
    } as $user

    // O valor a conferir COMECA sendo o de descarte, e so e trocado quando a
    // conta existe E TEM SENHA GRAVADA. Escrito nesta ordem, e nao como um
    // ramo com dois lados, porque o caminho sem conta e justamente o que
    // precisa estar garantido: se alguem mexer no ramo e ele deixar de
    // atribuir, o que sobra e o hash de descarte -- que recusa, e recusa
    // pagando o mesmo tempo.
    //
    // A SEGUNDA CONDICAO NAO E ZELO. `password` e OPCIONAL na tabela `user`
    // (`password? password`), entao conta sem senha nao e hipotese: e como
    // nasce o primeiro admin da clinica, criado a mao no painel do Xano (ver
    // Migration Plan do design.md). Sem esta guarda, `$hash_conferido` viria
    // vazio e `security.check_password` lancaria ERROR_FATAL "Invalid password
    // syntax." -- medido na tarefa 1.3 -- devolvendo 500 onde o e-mail
    // inexistente devolve 403. Seria um oraculo de existencia NOVO, criado
    // pelo proprio arquivo que veio fechar um, e dos barulhentos: basta
    // comparar o status. Caindo para o descarte, a conta sem senha recusa
    // igual a conta que nao existe, no mesmo tempo e com o mesmo corpo.
    //
    // As duas conferencias sao ANINHADAS, e nao um `&&` so: assim `$user.password`
    // nunca e avaliado com `$user` nulo, sem depender de o motor curto-circuitar
    // o `&&`. O `!= ""` acompanha o `!= null` porque o Xano grava string vazia,
    // e nao nulo, em coluna de texto omitida -- a mesma inferencia que o D4
    // registra sobre o `enum?` vazio.
    var $hash_conferido {
      value = $hash_descarte
    }

    conditional {
      if ($user != null) {
        conditional {
          if (($user.password != null) && ($user.password != "")) {
            var $hash_conferido {
              value = $user.password
            }
          }
        }
      }
    }

    // Roda sempre, nos dois casos, na mesma posicao da pilha. E este gesto, e
    // so ele, que faz o relogio parar de responder "esta conta existe".
    security.check_password {
      text_password = $input.password
      hash_password = $hash_conferido
    } as $senha_confere

    // UMA recusa para os dois casos: mesmo error_type, logo mesmo status, e a
    // MESMA string. Duas preconditions com mensagens diferentes refariam pelo
    // corpo o oraculo que acabou de ser fechado pelo relogio (design.md, D5,
    // invariante 3).
    //
    // O `$user != null` nao e redundante com a conferencia de senha: sem ele,
    // qualquer defeito que fizesse a comparacao contra o hash de descarte
    // passar criaria um token para uma conta que nao existe.
    precondition (($user != null) && ($senha_confere == true)) {
      error_type = "accessdenied"
      error = "Credenciais invalidas."
    }

    // Mesmo formato do auth/login do template e do tutor/cadastro: 24h, sem
    // extras.
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken

    // O metadata e um objeto MONTADO a mao. O template manda `$user` cru, e e
    // exatamente assim que o hash da senha e copiado para a tabela `event_log`
    // a cada entrada -- de onde `GET /logs/user/my_events` o devolve ao dono
    // da conta (design.md, D6). Aqui nao ha o que vazar porque o que se grava
    // foi escolhido campo a campo.
    //
    // So o SUCESSO e registrado. Registrar a recusa exigiria grava-la nos dois
    // casos, sempre, sob pena de reabrir a diferenca de tempo que este arquivo
    // existe para fechar -- e isso daria a qualquer um uma escrita de graca
    // numa tabela que ja esta pendente de politica de retencao.
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "entrar"
        metadata: {id: $user.id, email: $user.email, acao: "entrar"}
      }
    } as $evento_registrado
  }

  // Sem `role`, e sem mais nada: mesmas chaves que o auth/login do template
  // devolve hoje, para que trocar um pelo outro no cliente seja so trocar a
  // URL.
  response = {authToken: $authToken, user_id: $user.id}
}
