// Cadastra um colaborador da clinica.
//
// Mesma abertura obrigatoria dos demais (design.md, D2): sessao, prova de
// equipe, e so entao qualquer db.*. Numa ESCRITA isso pesa mais que numa
// leitura -- sem a prova, qualquer conta autenticada passa a escrever na folha
// de pessoal da clinica, e nao ha `where` de dono que limite o estrago, porque
// `colaborador` nao tem dono.
//
// Colaborador e REGISTRO, nao credencial (spec de colaboradores): este endpoint
// nao cria conta de acesso, nao chama `security.create_auth_token` e nao toca a
// tabela `user`. A proposta decidiu que as duas coisas sao separadas, e e
// justamente essa separacao que faz nao existir aqui coluna apontando para uma
// conta.
//
// O que o parser NAO cobra e esta pilha cobra (design.md, D10):
//
//   1. nome so de espacos -- `filters=trim` reduz "   " a "" DEPOIS de a
//      obrigatoriedade da entrada estar satisfeita, entao o Xano aceita a chave
//      presente e um colaborador nasceria sem nome. A change anterior achou
//      exatamente isso num POST de animal.
//   2. funcao fora do conjunto -- a coluna e `enum` e recusaria sozinha, mas
//      com um 500 cru do motor. A spec pede recusa com motivo informado.
//
// `funcao` entra como `text`, e nao como `enum`, de proposito: declarada enum,
// a recusa viria do tipo de entrada e a mensagem seria a do Xano. Declarada
// text, a recusa e esta precondition, com texto nosso.
query "equipe/colaboradores" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cadastra um colaborador da clinica"

  // `db.add` exige `data` como objeto LITERAL -- `db.patch` aceita variavel.
  // Entao cada campo e referenciado direto, e por isso o tipo da data importa:
  // `date` derruba o endpoint com 500 quando o campo e omitido, mesmo opcional.
  // `timestamp` tolera a ausencia.
  input {
    text nome filters=trim
    text funcao filters=trim
    text telefone? filters=trim
    email email? filters=trim|lower
    timestamp data_entrada?
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

    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do colaborador nao pode ficar em branco."
    }

    // Igualdade contra cada literal do conjunto, nunca negacao do que nao vale
    // (design.md, D4). Vazio, "Veterinario", "recepcionista" e qualquer erro de
    // digitacao caem todos do mesmo lado -- o lado negado. A forma por negacao
    // (`!= "recepcionista"`) le como se estivesse certa e passaria em revisao,
    // mas deixa entrar tudo que ninguem listou.
    precondition (($input.funcao == "veterinario") || ($input.funcao == "tosador") || ($input.funcao == "atendente")) {
      error_type = "inputerror"
      error = "Funcao invalida. Use veterinario, tosador ou atendente."
    }

    // `ativo` nao e entrada -- quem acaba de ser cadastrado esta na clinica.
    // Quem desliga e a alteracao, que tem o campo. A coluna ja tem padrao
    // `?=true`, e mesmo assim o valor vai LITERAL aqui: `pet_create.xs` e
    // `tutor_cadastro.xs` fazem o mesmo com `created_at`, e e a unica forma
    // cujo resultado o projeto de fato observou. Depender do padrao disparar no
    // insert custaria, se nao disparar, toda contratacao nascendo inativa sem
    // erro nenhum -- do tipo que ninguem repara ate a lista parecer certa e a
    // coluna nao.
    db.add colaborador {
      data = {
        created_at  : "now"
        nome        : $input.nome
        funcao      : $input.funcao
        telefone    : $input.telefone
        email       : $input.email
        data_entrada: $input.data_entrada
        ativo       : true
      }
    } as $novo
  }

  // Montada campo a campo, com o mesmo conjunto de chaves da listagem: assim a
  // tela que acabou de cadastrar ja tem a linha no formato em que vai rele-la.
  response = {
    id          : $novo.id
    nome        : $novo.nome
    funcao      : $novo.funcao
    telefone    : $novo.telefone
    email       : $novo.email
    data_entrada: $novo.data_entrada
    ativo       : $novo.ativo
  }
}
