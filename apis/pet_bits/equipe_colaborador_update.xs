// Altera um colaborador da clinica.
//
// Mesma abertura obrigatoria dos demais (design.md, D2): sessao, prova de
// equipe, e so entao qualquer db.*.
//
// O PADRAO `pick`, copiado de `pet_update.xs`: `$input` sozinho nao distingue
// "campo omitido" de "campo enviado vazio" -- o ausente chega como o padrao do
// tipo ("" ou 0) e uma alteracao de telefone apagaria funcao, e-mail e data de
// entrada. O corpo CRU diz quais chaves a requisicao de fato enviou, e so
// essas sao tocadas. Assim "os campos nao mencionados permanecem com os valores
// que tinham" (spec de colaboradores) e ESTRUTURAL, e nao uma promessa que
// alguem precisa lembrar de manter.
//
// Por que NAO ha `db.transaction` com lock aqui, diferente de `pet_update.xs`:
// la a transacao protege a janela entre a prova de POSSE e a gravacao -- se o
// vinculo mudasse no meio, a escrita cairia na ficha errada. Aqui a consulta
// anterior ao patch nao prova posse, prova EXISTENCIA, e so para que o
// identificador inexistente saia como notfound em vez de uma gravacao em nada.
// Ja foi medido que uma transacao com lock interrompida antes do commit deixa a
// linha presa; pagar esse preco por uma checagem de existencia nao compra nada.
//
// As guardas de nome e de funcao sao CONDICIONAIS porque a alteracao e parcial:
// quem nao envia o campo nao o esta esvaziando. Quem envia, esta -- e e esse o
// caso que o `pick` torna possivel e que o parser nao cobra (design.md, D10).
query "equipe/colaboradores/{colaborador_id}" verb=PATCH {
  api_group = "PetBits"
  auth = "user"
  description = "Altera os dados de um colaborador da clinica"

  input {
    int colaborador_id filters=min:1
    text nome? filters=trim
    text funcao? filters=trim
    text telefone? filters=trim
    email email? filters=trim|lower
    timestamp data_entrada?
    // Esta change nao tem exclusao de colaborador, de proposito: quem saiu da
    // clinica ainda e quem executou os servicos ja registrados. Desligar e
    // alterar `ativo`, e e por isso que ele e entrada aqui e nao no cadastro.
    bool ativo?
  }

  stack {
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    // Simetria de forma, nao seguranca (design.md, D2): a funcao lanca antes de
    // devolver qualquer coisa.
    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $corpo_cru

    var $dados {
      value = `$input|pick:($corpo_cru|keys)`|unset:"colaborador_id"
    }

    precondition (($dados|count) > 0) {
      error_type = "inputerror"
      error = "Informe ao menos um campo para alterar."
    }

    // `nome` e obrigatorio no cadastro; permitir esvazia-lo na alteracao
    // deixaria a linha sem identificacao nenhuma na lista da equipe, e hoje so
    // a validacao da tela segurava isso -- uma requisicao direta passava.
    conditional {
      if (($dados|has:"nome") == true) {
        precondition ((($dados|get:"nome")|trim) != "") {
          error_type = "inputerror"
          error = "O nome do colaborador nao pode ficar em branco."
        }
      }
    }

    // A mesma igualdade contra cada literal do cadastro (design.md, D4): se
    // esta guarda faltasse, a alteracao seria o caminho de contorno da recusa
    // que a criacao faz -- cadastra-se com "atendente" e troca-se depois.
    // Funcao vazia cai do lado negado junto com a desconhecida.
    conditional {
      if (($dados|has:"funcao") == true) {
        precondition ((($dados|get:"funcao") == "gerente") || (($dados|get:"funcao") == "veterinario") || (($dados|get:"funcao") == "tosador") || (($dados|get:"funcao") == "atendente")) {
          error_type = "inputerror"
          error = "Funcao invalida. Use gerente, veterinario, tosador ou atendente."
        }
      }
    }

    // `db.patch` recusa `where` e `join` (fato medido 4), entao a existencia e
    // conferida por uma consulta propria. Sem ela, alterar um identificador que
    // nao existe nao teria o que acusar, e a spec pede "nao encontrado".
    db.query colaborador {
      where = $db.colaborador.id == $input.colaborador_id
      output = ["id"]
      return = {type: "single"}
    } as $existente

    precondition ($existente != null) {
      error_type = "notfound"
      error = "Colaborador nao encontrado."
    }

    // Pelo id que a CONSULTA devolveu, nunca pelo id da requisicao -- a mesma
    // disciplina de `pet_update.xs`. Aqui os dois sao iguais por construcao; a
    // forma fica igual para que copiar este arquivo como modelo de uma escrita
    // com dono nao perca a parte que importa.
    db.patch colaborador {
      field_name = "id"
      field_value = $existente.id
      data = $dados
    } as $atualizado
  }

  response = {
    id          : $atualizado.id
    nome        : $atualizado.nome
    funcao      : $atualizado.funcao
    telefone    : $atualizado.telefone
    email       : $atualizado.email
    data_entrada: $atualizado.data_entrada
    ativo       : $atualizado.ativo
  }
}
