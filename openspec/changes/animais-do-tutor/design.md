# Design

## Context

Ver `proposal.md` — Why. O que condiciona o desenho:

- A tabela `tutor` já existe, com `id_user?` ligando à conta de acesso. O
  índice sobre `id_user` é **btree não único** — decisão forçada na change
  anterior pelo fato de o Xano gravar `0` em vínculo omitido.
- `auth = "user"` num endpoint dá `$auth.id`, o identificador da conta
  extraído do token. O token não carrega o papel.
- Medições já feitas nesta conta: o Xano grava **`0`, não nulo**, em coluna de
  vínculo omitida; `db.transaction { stack { ... } }` faz rollback de verdade.
- Plano gratuito: 10 requisições a cada 20 segundos, **por instância**.

Quatro abordagens para provar posse de dado foram desenhadas por ângulos
independentes e cada uma foi atacada por quem queria quebrá-la. Nenhuma foi
quebrada, nenhuma saiu ilesa. O que segue é a combinação que resultou disso.

## Goals / Non-Goals

**Goals:**

- Fixar o padrão de posse que as changes de agendamento e de histórico vão
  copiar. Esta change já é o caso de um salto (`pet → tutor → user`), não o
  caso fácil.
- Que o modo de falhar seja **barulhento**: um erro de implementação deve
  aparecer no primeiro teste, não numa auditoria.

**Non-Goals:**

- Acesso da equipe da clínica aos animais. O filtro desta change é de posse
  **direta**, e um tutor de balcão (sem conta) fica fora dele por construção.
  A equipe terá endpoints separados.
- Excluir animal, e qualquer decisão sobre o histórico de um animal excluído.

## Decisions

### D1 — Leitura nasce filtrada; escrita é prova + ação

A pergunta da change tem duas metades com respostas diferentes, e tratá-las
como uma só é o erro que este design existe para evitar.

**Leitura.** `db.query` com `join` até `tutor` e o dono dentro do `where`:

```
db.query pet {
  join = {
    tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
  }

  where = $db.tutor.id_user == $auth.id
  sort = {nome: "asc"}
  output = ["id", "nome", "especie", "raca", "data_nascimento", "peso", "observacoes"]
  return = {type: "list"}
} as $meus
```

Não existe instante em que o registro alheio esteja numa variável do endpoint
esperando conferência — então não há `if` para inverter nem `return` para
esquecer. `db.get` fica **proibido** nesta superfície: ele não filtra.

**Escrita.** Aqui a prova volta a ser prova, e não há como evitar. Medido no
parser oficial:

```
db.patch pet { field_name = "id"  where = ... }
  → The argument 'where' is not valid in this context
```

`db.patch`, `db.get`, `db.edit`, `db.del` e `db.add_or_edit` **recusam** `where`
e `join`; oferecem exatamente um par `field_name`/`field_value`. Então toda
escrita por identificador usa **três instruções dentro de uma transação**:

```
db.transaction {
  stack {
    db.query pet {
      join = {
        tutor: {type: "inner", table: "tutor", where: $db.pet.id_tutor == $db.tutor.id}
      }

      where = ($db.pet.id == $input.pet_id) && ($db.tutor.id_user == $auth.id)
      lock = true
      output = ["id"]
      return = {type: "single"}
    } as $meu

    precondition ($meu != null) {
      error_type = "notfound"
      error = "Animal nao encontrado."
    }

    db.patch pet {
      field_name = "id"
      field_value = $meu.id
      data = {...}
    } as $atualizado
  }
}
```

O `field_value` é `$meu.id` — o identificador que a prova devolveu —, **nunca**
`$input.pet_id` de novo.

*Por que isto precisa estar escrito por extenso:* a frase "a regra de acesso e
o acesso são a mesma instrução" é verdadeira só na leitura. Quem copiar a frase
para uma escrita bate no erro do parser, e o caminho de menor resistência é
**tirar a cláusula**, não acrescentar uma consulta — produzindo um PATCH sem
conferência nenhuma, que compila limpo e passa em revisão.

### D2 — Por que filtrar na consulta, e não conferir depois

Pelo modo de falhar. Se o `join` ou o `where` faltar, a listagem devolve os
animais de todo mundo e qualquer teste com duas contas percebe na hora. Uma
`precondition` esquecida devolve 200 com dado alheio **e passa em revisão**,
porque a primeira precondition continua visível e correta no topo do arquivo.

Custo também: 1 consulta para listar e 1 para obter, contra 2 e 2 da checagem
após leitura, e 2 e 2 de um resolvedor central. E a consulta filtrada nunca
traz a linha alheia para a memória do endpoint, para o log de requisição nem
para o depurador do Xano.

*Alternativa descartada — resolvedor central (`função que devolve quem pede`):*
cobra uma consulta a mais em **toda** leitura para entregar o que o join já traz
de graça, e não fecha a metade da escrita — só a enuncia errado também. O que ela
tem de insubstituível foi aproveitado em D4, onde o join não alcança.

### D3 — O dono `0` vira invisibilidade estrutural

O `inner join` descarta o órfão sozinho: um animal com `id_tutor = 0` não casa
com nenhuma linha de `tutor`, porque a chave primária começa em 1. O fato
medido passa a ser resolvido pelo motor, não por uma regra que alguém esquece.

Mas invisibilidade é perda silenciosa de dado, então as duas portas por onde o
`0` entra ficam fechadas por regra escrita:

- **`db.edit` e `db.add_or_edit` proibidos** em tabela com coluna de dono. Eles
  têm a mesma assinatura do `db.patch` — um caractere de diferença — e um
  `db.edit` cujo `data` omite `id_tutor` grava `0` e some com o animal, sem
  erro, numa edição legítima do próprio dono.
- **`precondition ($id_tutor > 0)` antes de todo `db.add`.**

Registrar explicitamente: **declarar `int id_tutor` sem `?` não protege disso.**
O único fato medido é que o Xano escreve `0`, e `0` satisfaz um inteiro
obrigatório. A obrigatoriedade da coluna é documentação de intenção, não
barreira.

**O preço, aceito e escrito:** um animal órfão some para todo mundo, inclusive
para a clínica, e nenhuma tela o alcança. Isso é falhar fechado, que é o certo
— mas quem encontrar o sintoma depois vai procurar defeito onde há decisão.
*Tarefa derivada para a change da equipe:* uma rota administrativa que procure
animais com `id_tutor = 0` **fora** do join.

### D4 — A resolução do tutor, só na escrita, com guarda de ambiguidade

`db.add` precisa do valor literal do dono, e join não produz valor para gravar.
Então o caminho de escrita resolve o tutor a partir do `$auth.id` — e é o único
lugar onde isso acontece.

A resolução **não** usa `return single`:

```
db.query tutor {
  where = $db.tutor.id_user == $auth.id
  output = ["id"]
  return = {type: "list"}
} as $fichas

precondition (($fichas.items|count) == 1) {
  error_type = "accessdenied"
  error = "Esta conta nao esta vinculada a um unico cadastro de tutor."
}
```

*Por quê:* `tutor.id_user` tem índice **não único** (change anterior, D3). Duas
fichas na mesma conta fariam o `return single` escolher uma arbitrariamente e
devolver um identificador positivo — exatamente o que uma checagem `> 0`
consideraria saudável. A conta passaria a escrever na ficha errada por via
legítima. Ambiguidade tem de falhar **alto**.

Isso vale a pena extrair para uma função reutilizável, porque as escritas de
agendamento e de histórico vão precisar da mesma resposta. Os parênteses em
volta do filtro são obrigatórios — sem eles o parser recusa.

### D5 — O dono nunca é entrada, em verbo nenhum

`id_tutor` não aparece em nenhum bloco `input`. Em consequência:

- **`dblink` proibido** em endpoint de escrita desta superfície. Ele transforma
  toda coluna da tabela em entrada, e `override = { id_tutor: {hidden: true} }`
  **não remove a chave de `$input`**.
- Toda coluna entra declarada uma a uma.
- O `data` de `db.add` e `db.patch` é mapa literal que nomeia só colunas de
  conteúdo, com `id_tutor` vindo exclusivamente da variável resolvida do token.
- Proibido também declarar `int id_tutor?` à mão — proibir só o `dblink` não
  basta.

O ataque que isto fecha: `PATCH /pet/12` com `id_tutor` no corpo doa o animal
para outra conta; com o próprio identificador no corpo de um animal alheio,
rouba.

### D6 — "Não existe" e "não é seu" dão a mesma resposta

Os dois casos saem como **não encontrado**, mesma mensagem e mesmo corpo, em
todos os endpoints que recebem um identificador — leitura **e escrita**.

*Por que o argumento de privacidade ganha:* identificadores são sequenciais, e
varrer de 1 a 9999 com respostas distinguíveis devolve o mapa de quais existem.
Mas o vazamento que importa não é a contagem: existência de registro numa
clínica veterinária é **dado de saúde por inferência**. A change anterior já
decidiu que esse tipo de confirmação não sai pela resposta.

*Por que o argumento de usabilidade não se sustenta aqui:* a tela só oferece
identificadores que vieram da própria listagem do tutor. Alguém digitando o
identificador de outro na URL não é cenário de usabilidade — é sondagem ou
defeito. E a informação que o diagnóstico precisa vai para o **registro do
servidor**, onde a distinção deve ser gravada.

**O PATCH também devolve "não encontrado".** Se a leitura for uniforme e a
escrita disser "sem permissão", o PATCH vira o oráculo que a leitura evitou — e
ninguém nota, porque "o GET está certo".

*Duas exceções deliberadas:* "esta conta não tem ficha de tutor" responde com
mensagem explícita **na criação** (é fato sobre a própria conta de quem pede,
não sobre registro de terceiro); e a **listagem** devolve lista vazia, não erro
— ler e não ter nada é diferente de tentar criar e não poder.

*Custo a registrar:* a resposta uniforme torna um defeito de vínculo e um
acesso indevido indistinguíveis **na resposta**. Por isso a distinção no
registro do servidor não é opcional — é a contrapartida que torna a decisão
pagável.

### D7 — O que o próprio Xano oferece: nada utilizável

Investigado para ninguém reinventar a armadilha:

- **`view` com `search` na definição da tabela** compila, e **não protege
  nada**: `db.query` não tem atributo para selecionar uma view, e a view roda no
  navegador de dados do painel, onde não existe token.
- **Middleware** não injeta `where`.
- **Addon** acrescenta campo, não remove linha.
- **`auth` na tabela** só aceita verdadeiro/falso.

Não há filtro por linha nativo. A proteção é convenção aplicada em cada
endpoint — e é por isso que D11 (teste com duas contas) não é recomendação, é
obrigação.

### D8 — Regras de escrita que o parser não cobra

Cada uma fecha um ataque que funcionou, e nenhuma é pega pelo validador:

- **`output` obrigatório** em toda `db.query` com `join`, listando só colunas
  da tabela de partida, e `id_tutor` **fora** dele. Sem `output`, o join leva
  documento, telefone, e-mail e endereço do tutor para dentro de cada linha da
  listagem, e o parser aprova sem reclamar.
- **`additional_where` e `override_sort` proibidos.** Eles injetam expressão
  vinda do corpo no mesmo nível do `where` que carrega a posse — e a listagem é
  exatamente onde uma caixa de busca vai aparecer.
- **`precondition ($auth.id > 0)` como primeira instrução** de todo endpoint
  privado. Custa zero consulta e faz o endpoint falhar fechado se algum dia for
  publicado sem `auth = "user"`.
- **`==` na comparação de posse — `===` NÃO existe em runtime.** O parser
  aceita `===` sem reclamar, mas o motor responde `ERROR_FATAL: Invalid name:
  ===` e o endpoint inteiro cai. Medido na tarefa 1.1. Esta regra substitui a
  recomendação original de usar comparação estrita, que teria quebrado todos os
  endpoints desta superfície.
- **Parênteses em toda expressão booleana** de `where` com mais de um operador.
  `A && B || C` compila sem eles, e no dia em que agendamento quiser "os meus ou
  os da clínica", um `||` sem parênteses anula o filtro de dono em silêncio.
- **Página validada no servidor**, com tamanho de página fixo.
- **Nenhuma coluna de `pet` leva índice único.** Decidido agora, enquanto a
  tabela não existe: duplicata estoura com erro do motor **abaixo** do `where`,
  então um índice único em `microchip` — candidato óbvio para quem desenhar a
  tabela depois — viraria oráculo de existência, confirmando que um animal é
  cliente da clínica sem nunca lê-lo.

### D9 — A correção no cadastro público

O `POST /tutor/cadastro` da change anterior devolve mensagem específica para
documento duplicado. Sendo público, isso confirma sem token nenhum se um
documento é de cliente da clínica. Passa a usar mensagem genérica única para
e-mail e para documento, com a distinção indo para o registro do servidor.

É a mesma decisão de D6 aplicada ao endpoint que a antecede — e é o berço de
todo identificador de tutor em que o resto do sistema confia.

### D10 — O que o grupo 1 mediu, e o que mudou por causa disso

As três premissas do desenho foram medidas com endpoints descartáveis antes de
escrever qualquer endpoint definitivo. Duas se confirmaram, e **três detalhes
contrariaram o que estava escrito**.

**Confirmado — a premissa central.** `where = $db.<tabela_juntada>.<coluna> ==
$auth.id` recorta de verdade em runtime, não só no parser. Medido com duas
contas e duas fichas: cada uma recebeu só a sua. O controle, sem o `where`,
devolveu as duas — é ele que prova que o recorte vem do `where`, e não de a base
ter um registro só.

**Corrigido 1 — `===` não existe em runtime.** O parser aceita, o motor responde
`ERROR_FATAL: Invalid name: ===`. A recomendação original de usar comparação
estrita teria derrubado todos os endpoints desta superfície logo no primeiro
uso. Vale `==`.

**Corrigido 2 — `output` e `paging` mudam de forma juntos.** Sem paginação, o
`output` lista nomes de coluna crus (`["id", "nome"]`) e a resposta é uma lista.
Com paginação, a raiz da resposta passa a ser o objeto de paginação, e o
`output` precisa ser prefixado (`["items.id", "items.nome"]`); os campos de
navegação entram no `output` se forem desejados. Misturar as duas formas devolve
**lista vazia, com status 200** — falha silenciosa, do pior tipo.

Nomes qualificados pela tabela (`["tutor.id"]`) devolvem `[[]]`, também sem
erro.

**Corrigido 3 — `totals` não vai solto no `return`.** Ele mora dentro de
`paging`.

**Confirmado — o vazamento do join é real e concreto.** Uma consulta com join e
**sem** `output` devolveu, em cada linha, `documento`, `telefone`, `email`,
`endereco` e `id_user` do tutor. Não é hipótese: foi observado. É o que torna o
`output` obrigatório, e não uma boa prática.

**`lock = true` trava de verdade — e isso tem um custo que precisa estar
escrito.** A medição da tarefa 1.2 não chegou ao número que eu queria (duas
chamadas concorrentes cronometradas), mas produziu evidência mais forte e menos
confortável: um endpoint descartável que tomava `lock = true` dentro de uma
transação e dormia 2 segundos teve a requisição abortada do lado do cliente, e a
linha ficou **inacessível para escrita por mais de dez minutos** — leituras
continuaram normais, toda tentativa de alteração ou remoção expirou.

Então o lock funciona. E o modo de falhar dele é: transação interrompida antes
do commit deixa a linha presa até o Xano reciclar a conexão.

*Por que isso não condena o padrão:* a transação do desenho é consulta +
`precondition` + `db.patch`, que roda em milissegundos. A janela só existiu
porque a medição pôs uma pausa artificial de 2 segundos lá dentro. Mas a regra
que sai daqui é concreta: **nada que demore — sem pausa, sem chamada externa,
sem laço — pode entrar dentro de um `db.transaction` com `lock`.**

**Decisão derivada:** a listagem desta change usa `output` **sem paginação**. A
lista de animais de um tutor não tem volume que a justifique, e cada forma extra
é uma chance a mais de cair na combinação que devolve vazio em silêncio. Quando
a paginação for necessária, ela entra como mudança própria, com a forma
prefixada e um teste que afirme o conjunto exato de chaves.

*Consequência na spec:* o cenário "Página inválida" perde objeto nesta change e
é removido do requisito de busca e ordenação — não há parâmetro de página para
validar. Ele volta com a paginação.

## Risks / Trade-offs

**A premissa central não foi medida em runtime** → `$db.<tabela_juntada>.<coluna>`
no `where` de topo: o parser aceita, o motor não foi exercitado. A abordagem
inteira depende disso. É a **primeira tarefa**, com endpoint descartável, antes
de qualquer outra — mesmo método que mediu o `0` e o rollback.

**`lock = true` dentro da transação não foi medido** → se não segurar a linha
até o commit, a janela entre a prova e o patch continua existindo. Hoje ela
está vazia (nada nesta superfície muda o dono), mas o domain-model já declara
que a troca de tutor vai existir.

**Escopo de variável criada dentro da transação** → o parser aceita responder
com ela de fora; o runtime é desconhecido. Plano B: responder com o resultado
da prova, ou reler após a transação por mais uma consulta.

**Duas fichas na mesma conta fazem a leitura devolver a união** dos animais das
duas. A guarda de ambiguidade protege a escrita, não a leitura. A raiz é
`tutor.id_user` sem índice único, e quem pode criar esse estado é a change que
vincular tutor de balcão a uma conta existente.

**Toda a proteção é convenção, não mecanismo** → nada impede publicar uma
listagem sem o join, um `db.get` onde deveria haver `db.query`, ou um PATCH sem
a prova. O parser não reclama de nenhum dos três. A única rede é o teste com
duas contas, por endpoint.

**O filtro é copiado em cada endpoint** e não dá para extrair para função,
porque o join vive dentro da consulta de cada um. Aceito conscientemente:
repetição auditável vale mais que um valor compartilhado que o chamador pode
esquecer de usar.

**O limite de requisições é por instância, não por usuário** → qualquer conta
legítima derruba a tela de todo mundo com 10 chamadas em 20 segundos. Não é
fechável nesta change; fica registrado.

**Identificadores sequenciais vazam volume de negócio por inferência.**
Severidade baixa, mas a decisão tem prazo: trocar o tipo do identificador só é
barato **antes** de a tabela existir. Fica escrito como escolha, não como
descuido.

## Migration Plan

Não há dados a migrar: a tabela de animais ainda não existe.

**Subida:** medir as três premissas com endpoint descartável; validar os `.xs`;
empurrar a tabela; empurrar os endpoints novos; republicar o cadastro corrigido
(D9); subir a aplicação.

**Volta atrás:** `git revert` e novo push dos `.xs` anteriores. O push do Xano é
por objeto e não transacional, então a volta é objeto a objeto — mais uma razão
para empurrar em lotes pequenos.
