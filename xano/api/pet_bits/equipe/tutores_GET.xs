//  Todos os tutores da clinica, para a equipe.
// 
//  ATENCAO ao que distingue este arquivo dos irmaos de `colaborador` e de
//  `servico` (design.md, D2): la a tabela nao tem coluna de dono nenhuma, aqui
//  tem -- `tutor.id_user` existe, e e exatamente a coluna que `me_tutor.xs` e
//  `tutor_do_token.xs` usam para recortar por quem pede. A consulta abaixo
//  DELIBERADAMENTE nao a usa (o motivo esta no paragrafo seguinte), e o efeito
//  e o mesmo dos irmaos: esta consulta nao tem `where` de posse, logo nao ha
//  filtro cuja ausencia alguem va notar, e o unico mecanismo de recusa e a
//  chamada a `exige_equipe`. Se ela sair da pilha, a base de clientes inteira
//  vai para qualquer conta autenticada, isto e, para qualquer visitante que se
//  cadastrou. Por isso ela vem antes de qualquer db.*: nada e lido antes de o
//  direito de ler estar estabelecido.
// 
//  A consulta NAO filtra por `id_user`, e isso e o requisito, nao esquecimento.
//  O tutor de balcao nunca usou o site e tem `id_user` gravado como 0 -- o Xano
//  grava 0, e nao nulo, em vinculo omitido. Qualquer filtro por conta de acesso,
//  inclusive um `id_user > 0` que pareceria higiene, sumiria com ele em silencio:
//  200, lista sem ele, nenhum erro. A spec de `tutores` tem cenario proprio
//  exigindo que ele apareca. E esta ausencia de filtro que distingue esta
//  consulta da do tutor, que nasce filtrada pelo dono -- e o caminho do tutor
//  fica identico, intocado (D1).
// 
//  O `output` leva documento, telefone, e-mail e endereco -- os quatro, e a
//  lista aqui tem de dizer os quatro, porque e ela que alguem vai reler ao
//  decidir se acrescenta um quinto. E o requisito da spec, e e
//  tambem o risco que o design registrou por escrito: uma credencial de equipe
//  comprometida e a base de clientes inteira, e esta change nao preve registro
//  de acesso por linha nem limite de volume. Nao ha mitigacao neste arquivo --
//  fica escrito aqui para que quem acrescentar coluna a esta lista saiba o que
//  esta aumentando.
// 
//  `id_user` fica de fora de proposito: a tela da equipe nao precisa do id da
//  conta de acesso de ninguem, e o que nao e carregado nao vaza para o depurador
//  nem para o `metadata` de um log -- que e exatamente como o hash de senha foi
//  parar no `event_log` pelo `auth/login` do template (D2).
// Lista todos os tutores da clinica, para a equipe
query "equipe/tutores" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
  }

  stack {
    // Falha fechada: se algum dia este endpoint for publicado sem auth, o id
    // chegaria zerado. Custa zero consulta.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }
  
    // A prova de equipe le o papel DO BANCO a cada requisicao -- o token nao
    // carrega papel, e de proposito: papel dentro do token congela por 24h e
    // rebaixar alguem nao teria efeito. Ela devolve o id da conta, nunca o
    // papel; se devolvesse o papel, o primeiro `if` por papel nasceria aqui,
    // que e precisamente o que o D1 existe para impedir.
    function.run "PetBits/exige_equipe" {
      input = {user_id: $auth.id}
    } as $id_conta
  
    // Simetria formal, NAO seguranca, e fica descrito como e: `exige_equipe`
    // lanca antes de devolver qualquer coisa. Esta linha so salva o caso de
    // alguem trocar o precondition interno dela por algo que devolva vazio em
    // vez de lancar. Ilusao de rede e pior que ausencia de rede.
    precondition ($id_conta > 0) {
      error_type = "accessdenied"
      error = "Sem permissao para esta area."
    }
  
    // So AQUI entra o primeiro db.*
    db.query tutor {
      sort = {nome: "asc"}
      return = {type: "list"}
      output = ["id", "nome", "documento", "telefone", "email", "endereco"]
    } as $tutores
  }

  response = $tutores
  guid = "08y4yTfwe_oZG3AxPhjiu8ZP_q8"
}