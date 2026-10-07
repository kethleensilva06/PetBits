//  A ficha de tutor de quem esta logado.
// 
//  O tutor e encontrado pelo $auth.id -- o id que o Xano extrai do token --, e
//  nunca por um id vindo do corpo ou da URL. E isso que torna impossivel pedir
//  a ficha de outra pessoa: nao ha onde informar de quem.
// 
//  Uma conta sem ficha (a equipe da clinica, por exemplo) recebe resposta vazia
//  em vez de erro: nao e falha, e ausencia. Isso e intencional, e o
//  `return single` abaixo preserva: sem linha casada, `$tutor` volta nulo,
//  igual ao que o `db.get` daqui devolvia.
// 
//  POR QUE ESTE ARQUIVO MUDOU (tarefa 8.7). Ele era o unico endpoint privado do
//  grupo sem `precondition ($auth.id > 0)`, e buscava com `db.get tutor` por
//  `id_user`. Com o id da conta chegando zerado, o filtro casaria com um tutor
//  de BALCAO -- foi medido que o Xano grava 0, e nao nulo, em coluna de vinculo
//  omitida -- e a resposta sairia com a ficha inteira: nome, documento,
//  telefone, e-mail e endereco de um cliente que nem conta tem.
// 
//  Hoje o `auth = "user"` segura isso e nao ha falha em producao. O problema e
//  que a garantia mora numa linha do cabecalho em vez de na pilha, e este
//  arquivo e curto o bastante para ser o modelo do qual alguem vai copiar o
//  proximo `me/*`. A falha dispara no dia da copia, nao hoje -- e nesse dia nao
//  haveria nada de errado na linha copiada para alguem reparar.
// Devolve a ficha de tutor vinculada a conta autenticada
query "me/tutor" verb=GET {
  api_group = "PetBits"
  auth = "user"

  input {
  }

  stack {
    // A mesma linha que pet_list.xs e tutor_do_token.xs ja tem, e pelo mesmo
    // motivo: id de conta zerado nao e sessao, e nao pode virar filtro. Custa
    // zero consulta.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }
  
    //  `db.query` com `where` explicito no lugar do `db.get` por
    //  `field_name`/`field_value`. O recorte passa a estar escrito da mesma
    //  forma que no resto do grupo, e essa e a razao principal: forma unica num
    //  arquivo so e o que faz a copia seguinte sair errada.
    // 
    //  A forma tambem e a unica que cresce. `db.get` RECUSA `where` e `join`
    //  (medido), entao no dia em que este recorte precisar de mais de uma
    //  coluna, quem estivesse com `db.get` teria de reescrever a consulta
    //  inteira -- que e quando o `where` se perde.
    // 
    //  Sem `output` de proposito, ao contrario de pet_list.xs: ali o join
    //  arrastava dado de terceiro para dentro da linha; aqui a linha e de quem
    //  esta pedindo, nao ha nada a esconder dela, e estreitar o conjunto
    //  mudaria a resposta que a tela ja consome.
    // 
    //  Registro honesto: com duas fichas na mesma conta, `single` escolhe uma
    //  arbitrariamente. E o mesmo comportamento do `db.get` que estava aqui. A
    //  ESCRITA nao aceita essa ambiguidade e falha alto (tutor_do_token.xs);
    //  esta leitura preserva o que havia, porque mudar comportamento visivel
    //  nao e o que a tarefa 8.7 pediu.
    db.query tutor {
      where = $db.tutor.id_user == $auth.id
      return = {type: "single"}
    } as $tutor
  }

  response = $tutor
  guid = "KXeWebQZJ8T37kdELsniEwHEJ6c"
}