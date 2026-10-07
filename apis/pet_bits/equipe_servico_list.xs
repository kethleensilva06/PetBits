// O catalogo de servicos da clinica, para a equipe.
//
// Esta familia e a primeira superficie SEM DONO do projeto (design.md, D2).
// Nenhuma coluna de `servico` aponta para uma conta, e isso e proposital: em
// `pet` a prova de posse E o `where`, entao esquecer o filtro e barulhento.
// Aqui nao ha `where` nenhum para esquecer, e o unico mecanismo de recusa e
// `exige_equipe`. Se a chamada a ela sair desta pilha o parser aprova o
// arquivo do mesmo jeito, e o catalogo inteiro passa a sair para qualquer
// conta autenticada -- isto e, para qualquer visitante que se cadastrou.
//
// Por isso a ordem e desenho, nao arrumacao: nada e lido antes de o direito de
// ler estar estabelecido. A guarda de repositorio (D9) existe para conferir
// exatamente esta ausencia, que e mais dificil de notar do que uma linha
// errada.
query "equipe/servicos" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista o catalogo de servicos da clinica, para a equipe"

  input {
  }

  stack {
    // Falha fechada: se este endpoint for publicado sem auth algum dia, o id
    // chegaria zerado e a prova abaixo receberia 0. Custa zero consulta.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    // A prova le o papel do banco a cada requisicao -- o token nao o carrega,
    // de proposito -- e devolve o ID DA CONTA, nunca o papel. Se devolvesse o
    // papel, o primeiro `if` por papel nasceria aqui no dia seguinte, que e
    // precisamente o que o D1 existe para impedir.
    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    // Registro honesto: isto e simetria de forma, nao seguranca. A funcao
    // lanca antes de devolver qualquer coisa. So salva o caso de alguem trocar
    // a precondition interna dela por algo que devolva vazio em vez de lancar.
    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // So AQUI, com o direito ja estabelecido, o banco e tocado.
    //
    // O `output` explicito nao e enfeite (D8): sem ele, toda coluna que alguem
    // acrescentar a `servico` depois -- custo interno, margem, observacao de
    // negociacao -- passa a sair na resposta sem ninguem decidir isso. Sem
    // paging, os nomes de coluna vao nus; com paging exigiriam o prefixo
    // `items.`, e misturar as duas formas devolve lista vazia com 200.
    db.query servico {
      sort = {nome: "asc"}
      output = ["id", "nome", "descricao", "preco", "duracao_minutos"]
      return = {type: "list"}
    } as $servicos
  }

  response = $servicos
}
