// Edita um animal do tutor autenticado.
//
// Padrao de ESCRITA do design.md (D1), e aqui a forma muda: `db.patch` NAO
// aceita `where` nem `join` -- medido no parser ("The argument 'where' is not
// valid in this context"). Entao a posse volta a ser provada por uma consulta,
// e so depois a acao acontece:
//
//   1. consulta-prova, com join e o `where` composto por id E dono, com lock;
//   2. precondition de nao encontrado;
//   3. db.patch pelo id que a PROVA devolveu -- nunca pelo id da requisicao.
//
// As tres dentro de uma transacao, e nada demorado la dentro: foi medido que
// uma transacao com lock interrompida antes do commit deixa a linha presa
// (design.md, D10).
//
// Sobre o `data`: ele carrega apenas os campos que a requisicao de fato enviou.
// `id_tutor` nao esta no `input`, entao nao existe em `$input` e nao ha como
// ele entrar aqui por esse caminho.
query "pet/{pet_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"
  description = "Edita um animal do tutor autenticado"

  input {
    int pet_id filters=min:1
    text nome? filters=trim
    text especie? filters=trim
    text raca? filters=trim
    timestamp data_nascimento?
    decimal peso?
    text observacoes? filters=trim
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    // O corpo cru diz quais campos a requisicao realmente enviou. Sem isto, um
    // campo ausente chegaria em $input como o padrao do tipo ("" ou 0) e a
    // edicao apagaria raca, peso e observacoes -- e observacoes e dado
    // clinico: alergias, cuidados especiais.
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $corpo_cru

    var $dados {
      value = `$input|pick:($corpo_cru|keys)`|unset:"pet_id"
    }

    precondition (($dados|count) > 0) {
      error_type = "inputerror"
      error = "Informe ao menos um campo para alterar."
    }

    db.transaction {
      stack {
        db.query pet {
          join = {
            tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
          }

          where = ($db.pet.id == $input.pet_id) && ($db.tutor.id_user == $auth.id)
          lock = true
          output = ["id"]
          return = {type: "single"}
        } as $meu

        // Mesmo "nao encontrado" da leitura: se a escrita dissesse "sem
        // permissao", ela viraria o oraculo de enumeracao que o GET evitou --
        // e ninguem notaria, porque "o GET esta certo" (design.md, D6).
        precondition ($meu != null) {
          error_type = "notfound"
          error = "Animal nao encontrado."
        }

        db.patch pet {
          field_name = "id"
          field_value = $meu.id
          data = $dados
        } as $atualizado
      }
    }
  }

  response = {
    id             : $atualizado.id
    nome           : $atualizado.nome
    especie        : $atualizado.especie
    raca           : $atualizado.raca
    data_nascimento: $atualizado.data_nascimento
    peso           : $atualizado.peso
    observacoes    : $atualizado.observacoes
  }
}
