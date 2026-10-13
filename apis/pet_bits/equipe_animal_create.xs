// Cadastro de animal PELA CLINICA, para um tutor que ela escolhe.
//
// ================= LEIA ANTES DE COPIAR ESTE ARQUIVO =================
//
// Este endpoint esta do lado da regra em que o DONO VEM DA REQUISICAO. Ele e
// a unica escrita do sistema assim, e isso e necessidade, nao descuido: a
// atendente cadastra o animal de outra pessoa, e a credencial dela nao aponta
// para tutor nenhum -- conta de equipe nao tem ficha.
//
// O OUTRO lado e o `pet_create.xs`, onde o dono vem de `tutor_do_token` e um
// `id_tutor` no corpo e IGNORADO. Se alguem copiar este arquivo como modelo
// de uma escrita do tutor e levar junto o `int id_tutor` da declaracao de
// entrada, o endpoint continua compilando, continua recusando quem nao tem
// sessao, e passa a aceitar que um tutor cadastre animal no nome de outro.
//
// Nenhuma guarda do repositorio pega isso. Este comentario e a defesa, e ela
// e fraca -- esta registrada como fraca no D1 do design.
//
// =====================================================================
//
// O que substitui "ignorar o que mandaram" e "CONFERIR o que mandaram": o
// tutor informado e procurado no banco antes de qualquer gravacao, e o animal
// e gravado pelo id que a CONSULTA devolveu.
query "equipe/animais" verb=POST {
  api_group = "PetBits"
  auth = "user"
  description = "Cadastra um animal da clinica para um tutor existente"

  // `db.add` exige `data` como objeto literal (fato medido 6), entao cada
  // campo e referenciado direto -- e por isso o tipo da data importa: com
  // `date`, um campo omitido derrubaria o endpoint com 500 (fato medido 5).
  input {
    int id_tutor
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

    // EQUIPE, nao gerencia: registrar o animal de quem chega e trabalho do
    // balcao.
    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // Zero nao e "ninguem": e o valor que o Xano grava em vinculo omitido
    // (fato medido 1), e um animal com dono zero fica invisivel para o tutor
    // POR CONSTRUCAO -- o `join` de `pet_list` o descarta. O backend teria
    // confirmado uma gravacao que, para quem deveria ve-la, nao existe.
    precondition ($input.id_tutor > 0) {
      error_type = "inputerror"
      error = "Informe de quem e o animal."
    }

    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "O nome do animal nao pode ficar em branco."
    }

    precondition ($input.especie != "") {
      error_type = "inputerror"
      error = "A especie nao pode ficar em branco."
    }

    // A conferencia que substitui o descarte. Ela e uma CONSULTA, nao um teste
    // de formato: o id pode ser um inteiro perfeitamente valido e nao
    // corresponder a tutor nenhum.
    db.query tutor {
      where = $db.tutor.id == $input.id_tutor
      output = ["id"]
      return = {type: "single"}
    } as $dono

    precondition ($dono != null) {
      error_type = "notfound"
      error = "Tutor nao encontrado."
    }

    // Grava pelo id que a CONSULTA devolveu, nunca pelo do input -- ainda que
    // aqui sejam iguais por construcao. E a mesma forma do `pet_update.xs`, e
    // ela esta aqui para que copiar este arquivo como modelo de uma escrita
    // COM dono nao perca justamente a parte que importa.
    db.add pet {
      data = {
        created_at     : "now"
        id_tutor       : $dono.id
        nome           : $input.nome
        especie        : $input.especie
        raca           : $input.raca
        data_nascimento: $input.data_nascimento
        peso           : $input.peso
        observacoes    : $input.observacoes
      }
    } as $novo
  }

  response = {
    id             : $novo.id
    id_tutor       : $novo.id_tutor
    nome           : $novo.nome
    especie        : $novo.especie
    raca           : $novo.raca
    data_nascimento: $novo.data_nascimento
    peso           : $novo.peso
    observacoes    : $novo.observacoes
  }
}
