// Cadastro de tutor de balcao: quem chega sem ter se cadastrado no aplicativo.
//
// O tutor criado aqui NAO recebe conta de acesso. `id_user` fica de fora do
// `data`, e o Xano grava 0 nessa coluna (fato medido 1) -- que e exatamente o
// valor que `tutor_do_token` e o `join` de `pet_list` tratam como "sem dono
// valido". Por isso a ficha existe para a clinica e nao alcanca o aplicativo.
//
// A ARMADILHA QUE ISTO CRIA (design.md da change `cadastro-de-balcao`, D5):
// esta pessoa fica com o documento ocupado e sem conta. Se ela tentar se
// cadastrar depois pelo aplicativo, o `tutor/cadastro` recusa -- documento ja
// existe -- com a mensagem generica que de proposito nao explica, e ela fica
// sem acesso sem saber por que. Resolver isso e ligar a conta nova a ficha
// existente, que e change propria: faze-lo pelo cadastro publico deixaria
// alguem reivindicar ficha alheia informando o CPF dela. A tela avisa na hora
// de criar; este arquivo registra o porque.
query "equipe/tutores" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cadastra um tutor de balcao, sem conta de acesso"

  input {
    text nome filters=trim
    text documento filters=trim
    text telefone? filters=trim
    email email? filters=trim|lower
    text endereco? filters=trim
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    // EQUIPE, nao gerencia: atender quem chega no balcao e o trabalho do
    // atendente. Manter o quadro de colaboradores e que e da gerencia.
    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // `filters=trim` reduz "   " a string vazia DEPOIS de a obrigatoriedade da
    // entrada ser satisfeita: a chave esta presente, entao o Xano aceita.
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do tutor nao pode ficar em branco."
    }

    // `123.456.789-01` e `12345678901` sao o MESMO documento. Sem normalizar,
    // os dois criam duas fichas para a mesma pessoa -- o que o indice unico
    // existe para impedir, contornado por pontuacao.
    //
    // Esta e a SEGUNDA copia desta regra: o `tutor_cadastro.xs` faz igual. As
    // duas precisam concordar, ou a porta de balcao vira a facil. A saida e
    // extrair para funcao, como `tutor_do_token` ja foi; esta change nao fez
    // isso, e a divida esta registrada no D3.
    var $documento {
      value = $input.documento|replace:".":""|replace:"-":""|replace:"/":""|replace:" ":""
    }

    precondition (($documento|strlen) == 11) {
      error_type = "inputerror"
      error = "O documento precisa ter 11 digitos."
    }

    // ANTES da gravacao, e nao depois. Duplicata em indice unico sai como
    // HTTP 500 "Duplicate record detected" (fato medido) -- erro cru em
    // ingles, onde a atendente precisa de "este documento ja esta cadastrado".
    //
    // O indice continua la: ele e a garantia de ultimo recurso, para a corrida
    // entre duas atendentes cadastrando a mesma pessoa ao mesmo tempo. Esta
    // conferencia e pela MENSAGEM; o indice e pela VERDADE.
    db.has tutor {
      field_name = "documento"
      field_value = $documento
    } as $documento_existe

    // EXPLICITA, ao contrario do cadastro publico. Nao e contradicao: a recusa
    // generica de la protege a pergunta "este CPF e cliente da clinica?" feita
    // por qualquer pessoa SEM credencial. Aqui quem pergunta e uma atendente
    // autenticada, que tem a lista inteira de tutores a um clique -- esconder
    // dela seria teatro. O que se esconde e funcao de quem pergunta, nao do
    // dado (design.md, D4).
    precondition ($documento_existe == false) {
      error_type = "inputerror"
      error = "Este documento ja esta cadastrado para outro tutor."
    }

    // `id_user` NAO entra: e o que faz esta ficha nascer sem conta.
    db.add tutor {
      data = {
        created_at: "now"
        nome      : $input.nome
        documento : $documento
        email     : $input.email
        telefone  : $input.telefone
        endereco  : $input.endereco
      }
    } as $novo
  }

  response = {
    id       : $novo.id
    nome     : $novo.nome
    documento: $novo.documento
    email    : $novo.email
    telefone : $novo.telefone
    endereco : $novo.endereco
  }
}
