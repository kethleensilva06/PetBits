// Lista os colaboradores da clinica, para a equipe.
//
// Esta e a primeira superficie do projeto SEM dono (design.md, D2): nenhuma
// coluna de `colaborador` aponta para uma conta. Em `pet` a prova de posse E o
// `where` -- a consulta nasce filtrada e nao existe instante em que dado alheio
// esteja numa variavel esperando conferencia. Aqui nao ha `where` de dono para
// esquecer, logo o unico mecanismo de recusa e a funcao `exige_equipe`. Se a
// chamada a ela sair desta pilha, a tabela inteira vai para qualquer conta
// autenticada -- isto e, para qualquer visitante que se cadastrou pelo site.
//
// Por isso a ordem e desenho, nao arrumacao: nada e lido antes de o direito de
// ler estar estabelecido. O parser aprova este arquivo com e sem a prova, e
// reparar na AUSENCIA de uma linha e mais dificil do que reparar numa linha
// errada -- e para isso que existe a guarda de repositorio (design.md, D9).
//
// O `output` e explicito pelo mesmo motivo do D8 da change anterior: o que nao
// e carregado nao vaza para o depurador nem para um metadata de log.
query "equipe/colaboradores" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Lista os colaboradores da clinica para a equipe"

  input {
  }

  stack {
    // Falha fechada: se este endpoint algum dia for publicado sem auth, o id
    // chega zerado e a prova nem comeca. Custa zero consulta.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    // Simetria de forma, nao seguranca, e fica registrado como e (design.md,
    // D2): a funcao lanca antes de devolver qualquer coisa. Esta linha so salva
    // o caso de alguem trocar o precondition interno dela por algo que devolva
    // vazio em vez de lancar. Ilusao de rede e pior que ausencia de rede.
    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // So AQUI entra o primeiro db.*
    //
    // Sem filtro por `ativo`: a spec pede "todos os colaboradores cadastrados",
    // e esconder o inativo da lista esconderia tambem o unico caminho de voltar
    // a ativa-lo, ja que esta change nao tem exclusao.
    db.query colaborador {
      sort = {nome: "asc"}
      output = ["id", "nome", "funcao", "telefone", "email", "data_entrada", "ativo"]
      return = {type: "list"}
    } as $colaboradores
  }

  response = $colaboradores
}
