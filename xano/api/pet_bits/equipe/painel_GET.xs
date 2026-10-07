//  O resumo da clinica numa requisicao so: quatro contagens, nenhuma linha.
// 
//  REGISTRO HONESTO, para quem for mexer: este endpoint e concessao a
//  plataforma, nao boa arquitetura (design.md, D7). Ele existe porque o plano
//  gratuito da 10 requisicoes a cada 20 segundos POR INSTANCIA. As quatro
//  listas no on_load do painel custariam 4 requisicoes em navegacao quente e 5
//  na carga fria -- metade do orcamento numa unica abertura de tela. Dois
//  colaboradores abrindo o painel ao mesmo tempo zeram a janela, e um F5 dentro
//  dos 20 segundos derrubaria o painel E a tela dos tutores junto, porque o
//  limite e por instancia.
// 
//  O preco de existir assim e que ele TENDE A VIRAR ENDPOINT-DEUS: cada widget
//  novo acrescenta uma consulta aqui e nada o limita. Quem vier acrescentar a
//  quinta contagem precisa decidir se ela paga o proprio custo, em vez de somar
//  mais um db.query ao fim da pilha porque "ja que estamos aqui".
// 
//  So contagens, de proposito. Mostrar tambem as primeiras linhas de cada lista
//  custaria exatamente as 4 requisicoes que este endpoint existe para evitar, e
//  no caso de `tutor` poria documento e contato de clientes numa tela de
//  recepcao que fica aberta o dia todo.
// 
//  Ganho secundario que vale registrar: a prova de equipe e UMA para as quatro
//  leituras. Nao ha como uma das quatro ter sido publicada sem prova, porque so
//  existe uma.
// So numeros. Nenhuma linha de nenhuma lista sai daqui -- nem "as tres
// ultimas", nem "o proximo agendamento". Quem precisar de linha abre a
// listagem, que custa a propria requisicao e tem o proprio `output`.
// Contagens da visao da clinica para o painel da equipe
query "equipe/painel" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
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
  
    //  A forma de contar e `return = {type: "count"}`, e nao output=["id"] mais
    //  `|count`: a forma por lista carregaria quatro listas de id inteiras para
    //  a memoria so para saber o tamanho delas.
    // 
    //  Ela so entrou depois de medida nesta conta (tarefa 1.1), conferida
    //  contra a forma por lista e inclusive em tabela com coluna enum. A
    //  medicao nao foi zelo: esta e a familia de construto cujo erro devolve
    //  LISTA VAZIA COM STATUS 200, e um painel mostrando zero colaboradores e
    //  zero animais seria lido como "a clinica esta vazia", nunca como bug.
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
  }

  response = {
    colaboradores: $total_colaboradores
    servicos     : $total_servicos
    tutores      : $total_tutores
    animais      : $total_animais
  }

  guid = "weVSG1up9LSwdH5o6_Lydo2fjt8"
}