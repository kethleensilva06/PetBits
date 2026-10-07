//  Os animais do tutor autenticado.
// 
//  Padrao de LEITURA do design.md (D1): a consulta ja nasce filtrada. O join faz
//  o salto pet -> tutor -> conta dentro da propria consulta, e o `where` compara
//  a ponta com o id do token. Nao existe instante em que um animal alheio esteja
//  numa variavel deste endpoint esperando conferencia -- entao nao ha `if` para
//  inverter nem `return` para esquecer.
// 
//  Se o join ou o `where` sumir, esta listagem devolve os animais de TODO MUNDO.
//  E barulhento de proposito: o teste com duas contas pega na hora. Uma
//  conferencia posterior esquecida devolveria 200 com dado alheio e passaria em
//  revisao.
// 
//  O `output` nao e enfeite (D8): sem ele, o join carrega documento, telefone,
//  e-mail e endereco do tutor para dentro de cada linha. Foi observado, nao
//  suposto. `id_tutor` fica de fora de proposito -- devolve-lo ao cliente
//  convidaria exatamente a devolucao que este desenho existe para impedir.
// Lista os animais do tutor vinculado a conta autenticada
query pet verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
  }

  stack {
    // Falha fechada: se algum dia este endpoint for publicado sem auth, o id
    // chegaria zerado e o filtro casaria com todos os tutores de balcao de uma
    // vez. Custa zero consulta.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }
  
    db.query pet {
      join = {
        tutor: {table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
      }
    
      where = $db.tutor.id_user == $auth.id
      sort = {nome: "asc"}
      return = {type: "list"}
      output = [
        "id"
        "nome"
        "especie"
        "raca"
        "data_nascimento"
        "peso"
        "observacoes"
      ]
    } as $meus
  }

  response = $meus
  guid = "VlQGuZs7LLRBtp9dMzC1M5SrgJE"
}