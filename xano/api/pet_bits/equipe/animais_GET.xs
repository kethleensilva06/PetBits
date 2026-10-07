//  Todos os animais atendidos pela clinica, com o tutor responsavel.
// 
//  Este arquivo e o `pet_list.xs` do tutor diferem em DUAS coisas, e a ordem
//  de importancia entre elas nao e a que a leitura rapida sugere.
// 
//  A primeira, e a que carrega a garantia: `pet_list.xs` tem
//  `where = $db.tutor.id_user == $auth.id` e este NAO TEM `where` nenhum. E o
//  `where` que e o recorte de posse la -- o join so faz o salto
//  pet -> tutor -> conta dentro da propria consulta, e o `where` compara a
//  ponta com o id do token (esta escrito assim no cabecalho do proprio
//  `pet_list.xs`, e vale repetir aqui porque "o inner join protege" e a
//  conclusao errada que este arquivo poderia sugerir a quem o copiasse). Aqui
//  o recorte de posse nao existe de proposito: a equipe enxerga a clinica
//  inteira, e quem recusa e `exige_equipe`, antes de qualquer db.*.
// 
//  A segunda e o tipo do join: `left` aqui, `inner` la. Os dois estao certos
//  pelo mesmo raciocinio aplicado a publicos diferentes. Em `pet_list.xs` o
//  `inner` nao e o que protege, mas acrescenta um descarte desejavel: animal
//  orfao nao pertence a tutor nenhum, logo nao aparece para tutor nenhum.
//  Aqui o animal orfao (`id_tutor` gravado como 0, porque o Xano grava 0 e nao
//  nulo em vinculo omitido) e justamente o registro que alguem precisa
//  consertar. Com `inner` ele sumiria EM SILENCIO: 200, lista sem ele, nenhum
//  erro -- e a leitura natural seria "esse animal nao existe" em vez de "esse
//  animal esta quebrado". E o mesmo modo de falha que fez a contagem de
//  animais do painel dispensar o join (D8), e a spec de `animais` tem cenario
//  proprio exigindo que o orfao apareca para a equipe.
// 
//  Trocar `left` por `inner` aqui nao quebra nada visivel: a lista continua
//  respondendo 200 e quase igual. Por isso esta escrito, e nao so feito.
// 
//  O nome do tutor vem por `eval` pelo mesmo motivo: no orfao o `left` nao casa
//  linha nenhuma, entao `tutor_nome` chega vazio em vez de derrubar a linha.
//  Vazio e o sintoma certo -- o animal aparece e se denuncia.
// 
//  O `output` e explicito porque sem ele o join despeja documento, telefone,
//  e-mail e endereco do tutor dentro de cada animal. Foi observado na change
//  anterior, nao suposto. Isto aqui e lista de animais; contato de cliente tem
//  endpoint proprio, com o risco registrado la.
// 
//  `pet_list.xs` nao foi tocado, e esse e o ponto inteiro do D1: publico novo
//  ganha endpoint novo, nenhum endpoint existente ganha um `if` por papel.
// Lista todos os animais da clinica com o tutor responsavel, para a equipe
query "equipe/animais" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
  }

  stack {
    // Falha fechada: se algum dia este endpoint for publicado sem auth, o id
    // chegaria zerado. Custa zero consulta.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }
  
    // Igual em todo endpoint de equipe, e antes de qualquer db.*: aqui a
    // consulta nao tem clausula de dono nenhuma, entao esta chamada e a unica
    // coisa entre a clinica inteira e qualquer conta autenticada (D2).
    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta
  
    // Simetria formal, NAO seguranca: `exige_equipe` lanca antes de devolver
    // qualquer coisa. Mesma observacao honesta de `equipe_tutor_list.xs`.
    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }
  
    // So AQUI entra o primeiro db.*
    db.query pet {
      join = {
        tutor: {
          table: "tutor"
          type : "left"
          where: $db.pet.id_tutor == $db.tutor.id
        }
      }
    
      sort = {nome: "asc"}
      eval = {tutor_nome: $db.tutor.nome}
      return = {type: "list"}
      output = [
        "id"
        "nome"
        "especie"
        "raca"
        "data_nascimento"
        "peso"
        "observacoes"
        "tutor_nome"
      ]
    } as $animais
  }

  response = $animais
  guid = "7H9zy8k8emve6AUobBkblM8oZyE"
}