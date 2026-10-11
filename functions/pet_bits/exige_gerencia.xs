// A prova de GERENCIA: irma de `exige_equipe`, um degrau acima.
//
// Por que duas funcoes e nao uma com parametro de nivel (design.md D3 desta
// change): um parametro cria a pergunta "e se ele vier errado, vazio ou
// ausente?", e responder isso direito exige mais uma guarda dentro da funcao.
// Foi exatamente o que derrubou a `Quick Start/enforce_role` do template, cujo
// portao nega quando a comparacao e verdadeira -- entao todo valor que a torne
// nao-verdadeira passa. Duas funcoes sem parametro nao tem essa pergunta: cada
// uma sabe UMA coisa, e quem escolhe e o endpoint.
//
// Quem chama esta: so os dois endpoints que MANTEM o quadro de colaboradores.
// Ler colaborador continua sendo de toda a equipe, e usa a irma. A guarda de
// repositorio confere isso nos dois sentidos -- trocar uma prova pela outra e
// a alteracao que ninguem nota lendo um diff.
function "PetBits/exige_gerencia" {
  description = "Falha com accessdenied se a conta nao for da gerencia; devolve o id dela"

  input {
    // Sempre o $auth.id do endpoint que chamou, NUNCA um id vindo do corpo ou
    // da URL. Se este parametro aceitasse um id informado pelo cliente, a
    // funcao deixaria de provar quem pede e passaria a provar quem foi
    // nomeado -- e qualquer conta passaria informando o id de uma gerente.
    int user_id
  }

  stack {
    // Falha fechada: id zerado e o valor que o Xano grava em vinculo omitido
    // (fato medido 1), nao "ninguem".
    precondition ($input.user_id > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // Papel do BANCO a cada requisicao, nunca do token. E `output` enxuto: o
    // que nao e carregado nao vaza para o depurador nem para um `metadata` de
    // log -- foi assim que o hash de senha foi parar no `event_log` pelo
    // `auth/login` do template.
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "role"]
    } as $conta

    precondition ($conta != null) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // UM literal, por igualdade. A forma e a mesma da irma, e pelo mesmo
    // motivo: `!= "staff"` leria igual, passaria em revisao, e deixaria passar
    // papel vazio e valor desconhecido. So a igualdade falha fechada.
    //
    // `==`, nunca `===`: o parser aceita os dois, o motor devolve ERROR_FATAL
    // no segundo (fato medido 2).
    precondition ($conta.role == "admin") {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }
  }

  // Mesma mensagem e mesmo error_type das recusas de `exige_equipe`, de
  // proposito: uma conta `staff` recusada aqui recebe exatamente o que um
  // tutor recebe la. Quem sonda nao aprende em que degrau a conta alheia esta
  // -- so que nao chegou neste.
  //
  // Devolve o ID, nunca o papel. Se devolvesse, o primeiro `if ($papel == ...)`
  // nasceria no endpoint chamador no dia seguinte, e e o ramo por papel que a
  // change passada inteira existiu para impedir. O id serve ao registro de
  // auditoria, que o papel nao serviria.
  response = $conta.id
}
