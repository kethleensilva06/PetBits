//  A prova de equipe: estabelece o direito de ler ANTES de qualquer leitura.
// 
//  Esta e a unica defesa da superficie de equipe, e isso e desenho, nao
//  descuido (design.md, D2). Em `pet` a linha tem dono, entao a consulta nasce
//  filtrada e a prova de posse E o `where`: se o filtro sumir, o teste de duas
//  contas acusa na hora. Em `colaborador` e `servico` nao existe coluna de
//  dono -- logo nao ha `where` para esquecer, e se a chamada a esta funcao sair
//  da pilha de um endpoint, a tabela inteira vai para qualquer conta
//  autenticada, isto e, para qualquer visitante que se cadastrou. Por isso ela
//  e chamada como segunda instrucao de todo endpoint `equipe/`, antes de
//  qualquer `db.*`: nada e lido antes de o direito de ler estar estabelecido.
// 
//  Nao reaproveita a `Quick Start/enforce_role` do template, e os motivos estao
//  inteiros no D3. Os dois que mais pesam:
// 
//  O portao dela NEGA quando a comparacao e verdadeira
//  (`if ($nivel_do_usuario < $nivel_exigido) throw`), entao todo valor que
//  torne a comparacao nao-verdadeira PASSA. Com papel em branco,
//  `$role_hierarchy|get:""` nao devolve 1 nem 2, e o veredito passa a depender
//  de como o runtime avalia essa comparacao. Isso NAO foi medido, e
//  deliberadamente nao foi (D3): a escolha certa e a formulacao que esta segura
//  sob os dois resultados possiveis. `precondition ($conta.role == "admin")`
//  PERMITE quando a comparacao e verdadeira, e a pergunta nao se coloca.
// 
//  E a mensagem de recusa dela devolve no corpo do 403 o papel exigido e o
//  papel real, que e o oraculo que este projeto gasta uma change inteira
//  fechando. Alem disso ela e objeto `xano:quick-start`: um re-push do template
//  a substitui.
//  Devolve o ID, nunca o papel (D1, D2). Se devolvesse o papel, ele ficaria
//  numa variavel do endpoint chamador e o primeiro `if ($papel == "admin")`
//  nasceria la no dia seguinte -- que e precisamente o que o desenho de
//  endpoints separados existe para impedir, porque um ramo por papel faz o
//  403 desaparecer e a sondagem vira indistinguivel de uso normal. O id ainda
//  serve ao registro de auditoria ("qual conta alterou este servico"), para o
//  que o papel nao serviria.
// 
//  As tres recusas acima saem IGUAIS -- mesmo error_type, mesma mensagem,
//  mesmo corpo. Id invalido, conta apagada e conta sem o papel certo sao
//  indistinguiveis de fora, de proposito: quem sonda nao pode aprender em que
//  estado esta a conta alheia. A distincao entre os tres casos pertence ao
//  registro do servidor, nunca a resposta.
// Confirma que a conta autenticada e da equipe e devolve o id dela
function "PetBits/exige_equipe" {
  input {
    // Sempre o $auth.id do endpoint que chamou, NUNCA um id vindo do corpo ou
    // da URL. Se um dia este parametro aceitar um id informado pelo cliente, a
    // funcao deixa de provar quem pede e passa a provar quem foi nomeado --
    // e qualquer tutor passa informando o id de um admin.
    int user_id
  }

  stack {
    // Falha fechada: id zerado nao e "ninguem", e o valor que o Xano grava em
    // vinculo omitido (fato medido 1). Deixa-lo seguir faria o `db.get` abaixo
    // procurar a linha de id 0 -- e o que a funcao decidisse sobre essa linha
    // seria decisao sobre uma conta que ninguem autenticou.
    precondition ($input.user_id > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }
  
    //  O papel vem do BANCO a cada requisicao, e nao do token: o token do
    //  projeto nao carrega papel (`extras = {}`) de proposito, porque papel
    //  dentro do token congela por 24 horas e rebaixar alguem nao teria efeito.
    // 
    //  O `output` e enxuto de proposito (D2). Esta funcao nao precisa de nome,
    //  de e-mail nem do objeto de troca de senha, e o que nao e carregado nao
    //  vaza para o depurador nem para um `metadata` de log. Nao e hipotese: foi
    //  assim que o hash de senha foi parar na tabela `event_log`, pelo
    //  `auth/login` do template, que poe "password" no output e manda o objeto
    //  inteiro para o log_event.
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "role"]
    } as $conta
  
    // Token tecnicamente valido de uma conta que foi apagada. Sem esta linha,
    // $conta seria nulo e a comparacao de papel abaixo decidiria sobre nada.
    precondition ($conta != null) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }
  
    //  IGUALDADE CONTRA O LITERAL. Esta linha e o coracao da funcao, e a forma
    //  dela importa mais que o conteudo -- leia antes de "simplificar".
    // 
    //  `user.role` e declarado `enum role?`, ou seja OPCIONAL. Conta sem papel
    //  nao e hipotese remota: e o estado em que o primeiro admin da clinica vai
    //  nascer, criado a mao no painel do Xano. As formas que leem como se
    //  estivessem certas e passariam em revisao:
    // 
    //    == "admin"   NEGA papel vazio, e nega tambem valor fora do enum
    //                 ("Admin", "administrador", erro de digitacao)
    //    != "member"  PERMITE papel vazio -- "nao e tutor, logo e equipe"
    //    != null      PERMITE se o vazio for "", que e o padrao que o Xano grava
    //    hierarquia   depende de como o runtime compara, e nega na direcao
    //                 errada (D3)
    // 
    //  So a primeira falha FECHADA. As outras tres falham ABERTAS, em silencio,
    //  e o sintoma e uma conta sem papel lendo a clinica inteira. `!= "member"`
    //  e a forma que um `if` por papel convida, porque dentro de um ramo o jeito
    //  natural de dizer e pela negacao -- e ela compila limpa no parser.
    // 
    //  A regra que vale para o projeto inteiro: papel se confere por igualdade
    //  com o valor esperado, nunca por negacao do outro valor nem por teste de
    //  nulidade (design.md, D4).
    // 
    //  `==`, e nao `===`: o parser aceita os dois, o motor devolve ERROR_FATAL
    //  no segundo (fato medido 2).
    precondition ($conta.role == "admin") {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }
  }

  response = $conta.id
  guid = "YDEQuKVRCrm0Z4YE_-m3m0ny-wM"
}