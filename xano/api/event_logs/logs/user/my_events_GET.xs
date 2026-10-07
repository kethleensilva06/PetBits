//  Os eventos da propria conta.
// 
//  O `output` EXPLICITO e a correcao desta change (design.md, D6). Sem ele, a
//  consulta devolvia as linhas CRUAS da tabela `event_log`, inclusive a coluna
//  `metadata` -- e varios endpoints do template gravam ali o objeto `$user`
//  inteiro:
// 
//    auth/login              metadata: $user    (ja despublicado nesta change)
//    auth/signup             metadata: $user    (ja despublicado nesta change)
//    reset/magic-link-login  metadata: $user1   (resultado de db.edit user)
//    reset/update_password   metadata: $user
// 
//  O `$user` desses arquivos carrega a coluna `password`, ou seja o HASH DA
//  SENHA. Resultado: o dono da conta lia de volta o proprio hash pedindo os
//  proprios eventos. Nao escala para outra conta -- o `where` e por dono --,
//  mas e segredo entregue ao cliente, e dado sensivel parado no log.
// 
//  Fechar a LEITURA resolve os quatro de uma vez, inclusive os dois de reset,
//  que continuam publicados e que esta change nao reescreve. E resolve tambem
//  as linhas que JA estao gravadas: `metadata` simplesmente nao sai mais daqui.
// 
//  O que isto NAO resolve, e fica dito: os hashes ja gravados continuam na
//  tabela. Apaga-los e a conversa de retencao do `event_log` que a change
//  anterior deixou pendente (D9) -- e que agora tem um motivo a mais.
// 
//  AVISO: este arquivo e objeto do template (`xano:quick-start`). Um re-push do
//  template o substitui e o vazamento volta, em silencio. Foi por isso que a
//  entrada nova (`PetBits/entrar`) nasceu como endpoint PROPRIO em vez de uma
//  edicao do `auth/login`; aqui nao havia essa escolha, porque o endpoint ja
//  existia e e o unico que serve esta leitura.
// Eventos da conta autenticada, sem o metadata
query "logs/user/my_events" verb=GET {
  api_group = "Event Logs"
  auth = "user"

  input {
  }

  stack {
    // Guarda de sessao explicita, como em todo endpoint privado do projeto.
    // Com `$auth.id` zerado o `where` abaixo casaria com toda linha de
    // `user_id` vazio -- e o Xano grava 0, nao nulo, em vinculo omitido
    // (fato medido 1). Hoje o `auth = "user"` ja garante o id; a guarda existe
    // para o dia em que este arquivo for copiado como modelo.
    precondition ($auth.id > 0) {
      error_type = "accessdenied"
      error = "Sessao invalida."
    }
  
    // `metadata` fica DE FORA. Sem paging, os nomes de coluna vao nus; com
    // paging exigiriam o prefixo `items.`, e misturar as duas formas devolve
    // lista vazia com status 200 (fato medido 4).
    db.query event_log {
      where = $db.event_log.user_id == $auth.id
      sort = {created_at: "desc"}
      return = {type: "list"}
      output = ["id", "created_at", "action"]
    } as $user_events
  }

  response = $user_events
  tags = ["xano:quick-start"]
  guid = "HrMfUin8ORMaV9E5wiWgeby9H5g"
}