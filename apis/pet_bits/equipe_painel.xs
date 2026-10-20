// O painel da clinica numa requisicao so: quatro contagens, a agenda do dia e
// os pedidos que esperam a equipe (change `painel-do-dia`).
//
// REGISTRO HONESTO, para quem for mexer: este endpoint e concessao a
// plataforma, nao boa arquitetura (change `operacao-da-clinica`, D7). Ele
// existe porque o plano gratuito da 10 requisicoes a cada 20 segundos POR
// INSTANCIA, e o painel e a tela inicial da equipe: cada chamada a mais aqui
// sai de toda abertura de painel, de todo colaborador, o dia todo.
//
// O preco de existir assim e que ele TENDE A VIRAR ENDPOINT-DEUS. A change
// `painel-do-dia` acrescentou duas coisas, e cada uma paga o proprio custo
// (design.md, D1): a agenda do dia, que e a pergunta que o painel existe para
// responder, e tres contagens de pedido, sem linha. Quem vier acrescentar a
// proxima precisa fazer a mesma conta, em vez de somar mais um db.query ao fim
// da pilha porque "ja que estamos aqui".
//
// O que continua PROIBIDO aqui: telefone, documento e endereco de tutor. Esta
// e uma tela de recepcao que fica aberta o dia todo (design.md, D3). Quem
// precisa ligar abre a Agenda, que tem o telefone.
//
// Ganho secundario que vale registrar: a prova de equipe e UMA para todas as
// leituras. Nao ha como uma delas ter sido publicada sem prova, porque so
// existe uma.
query "equipe/painel" verb=GET {
  api_group = "PetBits"
  auth = "user"
  description = "Contagens, agenda do dia e pedidos esperando, para o painel da equipe"

  input {
    // Inicio do dia (meia-noite em Sao Paulo), em ms UTC, como em
    // `equipe/agenda`: a tela ja calcula o dia (design.md, D2).
    timestamp dia
  }

  stack {
    // Nada e lido antes de o direito de ler estar estabelecido (design.md,
    // D2). Aqui o motivo e mais forte que no lado do tutor: `colaborador` e
    // `servico` nao tem coluna de dono, logo nao existe `where` de posse para
    // esquecer, e a prova e o UNICO mecanismo de recusa desta superficie. Se
    // ela sair da pilha, a clinica inteira vai para qualquer conta
    // autenticada -- isto e, para qualquer visitante que se cadastrou.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }

    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta

    // Simetria formal, nao seguranca: `exige_equipe` lanca antes de devolver
    // qualquer coisa (design.md, D2). Isto so cobre o dia em que alguem trocar
    // o precondition de dentro dela por algo que devolva vazio em vez de
    // lancar. Custa zero e fica, mas fica descrito como e.
    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }

    // A forma de contar e `return = {type: "count"}`, e nao output=["id"] mais
    // `|count`: a forma por lista carregaria quatro listas de id inteiras para
    // a memoria so para saber o tamanho delas.
    //
    // Ela so entrou depois de medida nesta conta (tarefa 1.1), conferida
    // contra a forma por lista e inclusive em tabela com coluna enum. A
    // medicao nao foi zelo: esta e a familia de construto cujo erro devolve
    // LISTA VAZIA COM STATUS 200, e um painel mostrando zero colaboradores e
    // zero animais seria lido como "a clinica esta vazia", nunca como bug.
    db.query colaborador {
      return = {type: "count"}
    } as $total_colaboradores

    db.query servico {
      return = {type: "count"}
    } as $total_servicos

    // Sem `where` de vinculo: o tutor de balcao (`id_user` gravado como 0) e
    // cliente da clinica como qualquer outro e conta aqui. Esta contagem e a
    // da clinica, nao a de quem usa o site.
    db.query tutor {
      return = {type: "count"}
    } as $total_tutores

    // A contagem de animais e `db.query pet` SEM join ate `tutor`, e isso e
    // decisao, nao esquecimento (design.md, D8). Um inner join descartaria em
    // silencio o animal orfao -- aquele com `id_tutor` gravado como 0, que o
    // Xano produz em vinculo omitido --, e contagem que esconde o registro
    // quebrado e pior que contagem nenhuma: ninguem procura o que o numero nao
    // acusa. E o mesmo motivo pelo qual `equipe_animal_list.xs` usa `left` e
    // nao `inner`.
    db.query pet {
      return = {type: "count"}
    } as $total_animais

    var $fim_do_dia {
      value = $input.dia + 86400000
    }

    // Quem vem hoje (design.md, D3). Os cancelados ficam de fora: o painel
    // responde "quem vem hoje", e a Agenda continua mostrando todos. Sem o
    // telefone do tutor, que `equipe/agenda` devolve.
    db.query agendamento {
      join = {
        pet        : {type: "left", table: "pet", where: $db.agendamento.id_pet == $db.pet.id}
        tutor      : {type: "left", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
        servico    : {type: "left", table: "servico", where: $db.agendamento.id_servico == $db.servico.id}
        colaborador: {type: "left", table: "colaborador", where: $db.agendamento.id_colaborador == $db.colaborador.id}
      }

      where = (($db.agendamento.inicio > $input.dia) || ($db.agendamento.inicio == $input.dia)) && ($fim_do_dia > $db.agendamento.inicio) && ($db.agendamento.situacao != "cancelado")
      eval = {
        pet_nome         : $db.pet.nome
        pet_especie      : $db.pet.especie
        tutor_nome       : $db.tutor.nome
        servico_nome     : $db.servico.nome
        profissional_nome: $db.colaborador.nome
      }

      sort = {inicio: "asc"}
      output = ["id", "inicio", "fim", "situacao", "pet_nome", "pet_especie", "tutor_nome", "servico_nome", "profissional_nome"]
      return = {type: "list"}
    } as $agenda_do_dia

    // Os pedidos que esperam a equipe (design.md, D4). `enviado` nao entra:
    // esta com a entrega, nao com a clinica. So contagens, sem linha.
    db.query pedido {
      where = $db.pedido.situacao == "pendente"
      return = {type: "count"}
    } as $pedidos_pendentes

    db.query pedido {
      where = $db.pedido.situacao == "pago"
      return = {type: "count"}
    } as $pedidos_pagos

    db.query pedido {
      where = $db.pedido.situacao == "pronto_retirada"
      return = {type: "count"}
    } as $pedidos_prontos
  }

  // Contagens, a agenda do dia e as contagens de pedido. Nenhum contato de
  // tutor sai daqui.
  response = {
    colaboradores  : $total_colaboradores
    servicos       : $total_servicos
    tutores        : $total_tutores
    animais        : $total_animais
    agenda         : $agenda_do_dia
    pedidos_pendentes: $pedidos_pendentes
    pedidos_pagos  : $pedidos_pagos
    pedidos_prontos: $pedidos_prontos
  }
}
