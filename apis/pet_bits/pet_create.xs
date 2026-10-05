// Cadastra um animal para o tutor autenticado.
//
// `id_tutor` NAO aparece no bloco `input` (design.md, D5). Nao e omissao: e a
// defesa. Nada que o cliente mande pode virar o dono, porque o dono nao e uma
// entrada deste endpoint. Por isso tambem nao ha `dblink` aqui -- ele
// transformaria toda coluna da tabela em entrada, e `override hidden` nao
// remove a chave de $input.
//
// O dono vem da funcao, que falha alto se a conta nao tiver exatamente uma
// ficha de tutor (design.md, D4).
query pet verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cria um animal para o tutor vinculado a conta autenticada"

  // `db.add` exige `data` como objeto literal -- `db.patch` aceita variavel.
  // Entao aqui cada campo e referenciado diretamente, e por isso o tipo da
  // data importa: com `date`, um campo omitido derrubaria o endpoint.
  input {
    text nome filters=trim
    text especie filters=trim
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

    function.run "PetBits/tutor_do_token" {
      input = {user_id: $auth.id}
    } as $id_tutor

    // Defesa em profundidade contra o `0`: um animal gravado com dono zero
    // seria invisivel para sempre, inclusive para a clinica, e o backend teria
    // confirmado uma gravacao que para o sistema nao existe (design.md, D3).
    precondition ($id_tutor > 0) {
      error_type = "accessdenied"
      error = "Esta conta nao tem um cadastro de tutor para vincular o animal."
    }

    // `filters=trim` reduz "   " a string vazia DEPOIS de a obrigatoriedade da
    // entrada ser satisfeita -- a chave esta presente, entao o Xano aceita. Sem
    // estas duas guardas, um animal nasce sem nome por requisicao direta.
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do animal nao pode ficar em branco."
    }

    precondition ($input.especie != "") {
      error_type = "inputerror"
      error = "A especie nao pode ficar em branco."
    }

    db.add pet {
      data = {
        created_at     : "now"
        id_tutor       : $id_tutor
        nome           : $input.nome
        especie        : $input.especie
        raca           : $input.raca
        data_nascimento: $input.data_nascimento
        peso           : $input.peso
        observacoes    : $input.observacoes
      }
    } as $novo
  }

  // A resposta e montada campo a campo, com o mesmo conjunto de chaves da
  // listagem: devolver id_tutor convidaria exatamente a devolucao que este
  // desenho existe para impedir.
  response = {
    id             : $novo.id
    nome           : $novo.nome
    especie        : $novo.especie
    raca           : $novo.raca
    data_nascimento: $novo.data_nascimento
    peso           : $novo.peso
    observacoes    : $novo.observacoes
  }
}
