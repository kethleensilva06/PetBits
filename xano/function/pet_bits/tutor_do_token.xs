//  Resolve qual tutor e o dono da requisicao, a partir do id da conta.
// 
//  Existe so para o caminho de ESCRITA. Na leitura, o join ate tutor ja faz o
//  salto dentro da propria consulta e esta funcao so cobraria uma consulta a
//  mais pelo que vem de graca (design.md, D2 e D4). O `db.add` e que precisa de
//  um valor literal para gravar, e join nao produz valor.
// 
//  Nao usa `return single`. A coluna `tutor.id_user` tem indice btree NAO unico
//  -- decisao forcada na change anterior pelo fato de o Xano gravar 0 em vinculo
//  omitido. Com duas fichas na mesma conta, `single` escolheria uma
//  arbitrariamente e devolveria um id positivo, que e exatamente o que uma
//  checagem `> 0` consideraria saudavel: a conta passaria a escrever na ficha
//  errada por via legitima. Ambiguidade tem de falhar ALTO.
// Devolve o id do tutor vinculado a conta, ou falha se nao houver exatamente um
function "PetBits/tutor_do_token" {
  input {
    // Sempre o $auth.id do endpoint que chamou
    int user_id
  }

  stack {
    // Falha fechada: se o id da conta chegar zerado, o filtro casaria com
    // todos os tutores de balcao de uma vez (design.md, D8).
    precondition ($input.user_id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }
  
    db.query tutor {
      where = $db.tutor.id_user == $input.user_id
      return = {type: "list"}
      output = ["id"]
    } as $fichas
  
    // Os parenteses em volta do filtro sao obrigatorios: sem eles o parser
    // recusa a expressao.
    precondition (($fichas|count) == 1) {
      error_type = "accessdenied"
      error = "Esta conta nao esta vinculada a um unico cadastro de tutor."
    }
  
    var $tutor_id {
      value = $fichas[0].id
    }
  
    // Defesa em profundidade: um id zerado aqui significaria ficha gravada sem
    // vinculo valido, e deixa-lo passar criaria um animal invisivel para
    // sempre (design.md, D3).
    precondition ($tutor_id > 0) {
      error_type = "accessdenied"
      error = "O cadastro de tutor desta conta esta incompleto."
    }
  }

  response = $tutor_id
  guid = "If0r0VVkUxIiaPMUI_yQh8MhHQE"
}