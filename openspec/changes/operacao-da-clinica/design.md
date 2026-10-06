# Design

## Context

Ver `proposal.md` — Why. O que condiciona o desenho:

- O papel vive em `user.role`, declarado **`enum role?`** em
  `tables/898256_user.xs` — ou seja, **opcional**. Conta sem papel não é
  hipótese remota: é o estado em que o primeiro admin da clínica vai nascer,
  criado à mão no painel do Xano, porque a proposta decidiu que promover
  alguém fica fora da aplicação.
- O token não carrega o papel (`extras = {}`), e isso não muda: papel dentro
  do token congela por 24 horas e rebaixar alguém não teria efeito.
- A change anterior fixou o padrão de **posse**: a consulta nasce filtrada
  pelo dono. Esta change é a primeira superfície **sem dono** — nenhuma coluna
  de `colaborador` ou de `servico` aponta para uma conta.
- Plano gratuito: 10 requisições a cada 20 segundos, **por instância**. O
  painel da equipe é a primeira tela do projeto com risco real de se
  auto-estourar.

Três desenhos independentes foram feitos para as perguntas em aberto, cada um
atacado por quem queria quebrá-lo. **Os três convergiram em endpoints
separados — inclusive o que foi designado para defender o ramo por papel.**
O que segue é o que resultou disso, com as afirmações sobre arquivos do
template conferidas uma a uma na leitura dos próprios arquivos.

## Goals / Non-Goals

**Goals:**

- Fixar o padrão de **autorização por papel** que as changes de agendamento e
  de histórico vão copiar, do mesmo jeito que a change anterior fixou o padrão
  de posse.
- Que a recusa seja **estrutural**: nenhum caminho em que ausência de papel,
  valor desconhecido ou erro de digitação seja tratado como permissão.
- Que o painel da equipe caiba no orçamento de requisições **por construção**,
  e não por cuidado de quem revisa.

**Non-Goals:**

- Escrita de animal ou de tutor pela equipe. Esta change dá **leitura** da
  visão da clínica; a escrita tem um desenho próprio que não foi feito (ver
  Risks).
- Ligar `colaborador` a `user`. A proposta já decidiu que são coisas
  separadas.
- Corrigir o oráculo de CPF do cadastro público — tem change própria.

## Decisions

### D1 — Endpoints separados por público, nunca ramo por papel

Toda operação da clínica vive em endpoint próprio, com prefixo `equipe/` e
arquivo próprio: `apis/pet_bits/equipe_colaborador_*.xs`,
`equipe_servico_*.xs`, `equipe_tutor_list.xs`, `equipe_animal_list.xs`,
`equipe_painel.xs`. Nenhum endpoint existente ganha um `if` por papel.

A alternativa era um endpoint por recurso com um ramo dentro
(`if ($conta.role == "admin") { consulta ampla } else { consulta filtrada }`).
Ela foi desenhada e atacada a sério. **O argumento que a derruba não é
estético, é observável:**

> Com o ramo, **o 403 desaparece**. Um tutor que chama `GET /pet` tentando
> alcançar a clínica recebe **200 com os animais dele**. A tentativa de
> alcançar a superfície da clínica fica indistinguível de uso normal, e não
> deixa linha nenhuma no registro.

Os outros modos de falhar de um ramo são barulhentos — alguém vê dado demais,
alguém reclama. Este é silencioso dos dois lados: quem sonda não é notado, e
quem opera não tem o que olhar. Com endpoints separados, a mesma tentativa é
um 403 em `equipe/animais`, que é exatamente a linha que se quer no registro.

Dois corolários:

- **O ramo não economiza requisição nenhuma.** Isto é confundido com
  frequência: o painel faz as mesmas quatro chamadas tendo um endpoint ou dois
  por recurso. Consolidar **papéis** e consolidar **recursos** são eixos
  diferentes, e só o segundo toca a cota (D7).
- **Separar é o que torna a guarda de repositório possível** (D9). Um script
  consegue exigir "todo arquivo `equipe_*.xs` chama a prova". Não consegue
  exigir "todo ramo dentro deste arquivo preserva o `where`".

**A regra da change anterior fica reformulada.** O que estava escrito —
"um ramo por papel dentro deste é como se perde a garantia" — é largo demais,
e regra que parece superstição é a primeira a ser contornada. A regra precisa
que entra no projeto:

> **Nenhum ramo por papel pode mudar o `where`, o `join` ou o `output` de uma
> consulta.**

Ramificar a *apresentação* é normal. Ramificar o *recorte do dado* é onde a
garantia morre.

### D2 — A prova de equipe: função própria, igualdade contra o literal

`functions/pet_bits/exige_equipe.xs`, chamada como **segunda instrução** de
todo endpoint de equipe, sempre na mesma forma:

```
precondition ($auth.id > 0) { ... }

function.run "PetBits/exige_equipe" {
  input = {user_id: $auth.id}
} as $id_conta
```

A função lê o papel **do banco** a cada requisição, com `output = ["id",
"role"]`, e compara por **igualdade contra o literal `"admin"`**. Devolve o
**id da conta, nunca o papel**.

Três escolhas dentro disso, cada uma com motivo:

**A ordem é desenho, não arrumação.** Esta superfície é o oposto da de
animais. Em `pet` a linha tem dono, então a consulta nasce filtrada e a prova
de posse **é** o `where`. Em `colaborador` não existe dono — logo **não há
`where` para esquecer**, e o único mecanismo de recusa é a função. Se ela sair
da pilha, a tabela inteira vai para qualquer conta autenticada, isto é, para
qualquer visitante que se cadastrou. Por isso ela vem antes de qualquer
consulta: nada é lido antes de o direito de ler estar estabelecido.

**Devolve o id, não o papel.** Se devolvesse o papel, ele ficaria numa
variável do endpoint chamador e o primeiro `if` por papel nasceria no dia
seguinte — que é precisamente o que o D1 existe para impedir. O id serve ao
registro de auditoria ("quem alterou este serviço"), que o papel não serviria.

**O `output` é enxuto de propósito.** Esta função não precisa de nome, de
e-mail nem do objeto de troca de senha. O que não é carregado não vaza para o
depurador nem para um `metadata` de log — que é exatamente como o hash de
senha foi parar na tabela `event_log` pelo `auth/login` do template (D6).

**Por que a prova não vira um `join` dentro da consulta**, truque que funciona
na leitura do tutor: ali o recorte é sobre a **linha**; aqui é sobre **quem
pede**, e nenhuma coluna de `colaborador` aponta para uma conta. Daria para
forçar um `join` até `user` com `where = $db.user.role == "admin"`, e isso
pouparia a consulta extra, mas (a) devolveria `200 []` para um tutor,
indistinguível de "a clínica não tem colaboradores" — o sintoma que esta
change existe para matar; (b) `db.add`, `db.patch` e `db.del` **recusam**
`where` e `join` (fato medido 4), então a escrita precisaria de outro
mecanismo — e dois mecanismos de prova na mesma superfície é exatamente como
alguém copia o arquivo de leitura como modelo de uma escrita e publica sem
prova nenhuma.

**Registro honesto:** a `precondition ($id_conta > 0)` depois do `function.run`
é simetria formal, **não segurança** — a função lança antes de devolver
qualquer coisa. Ela só salva o caso em que alguém troque o `precondition`
interno por algo que devolva vazio em vez de lançar. Custa zero e fica, pela
consistência de forma com `pet_create.xs`, mas fica descrita como é. Ilusão de
rede é pior que ausência de rede.

### D3 — Por que não a `Quick Start/enforce_role` do template

O template já traz uma função de papel. Ela foi lida inteira
(`functions/quick_start/347166_enforce_role.xs`) e **não serve**. Seis
motivos, todos verificáveis no arquivo:

**1. O portão dela falha na direção errada.** O gesto é:

```
conditional {
  if ($user_role_level < $required_role_level) { throw { ... } }
}
```

Ele **nega quando a comparação é verdadeira**. Todo valor que torne a
comparação não-verdadeira **passa**. Com papel em branco,
`$role_hierarchy|get:""` não devolve 1 nem 2, e o veredito passa a depender de
como o runtime avalia essa comparação. **Isso não foi medido, e
deliberadamente não foi medido**: a escolha certa é a formulação que está
segura sob os dois resultados possíveis. `precondition ($conta.role ==
"admin")` **permite quando a comparação é verdadeira**, e a pergunta não se
coloca.

**2. Hierarquia não é o modelo deste domínio.** `{admin: 2, member: 1}` com
`<` só sabe dizer "pelo menos". Aqui tutor e equipe são plateias **disjuntas**:
a conta de equipe não tem ficha de tutor, então ela não "vê os animais dela" —
ela não tem animais. A função do template é incapaz de exprimir "exatamente
cliente", e no dia em que alguém escrever `enforce_role(user, "member")`
querendo "só tutores", **toda conta de equipe passa**.

**3. A mensagem vaza o papel no corpo do 403:**
`"... Required: " ~ $input.required_role ~ ", Actual: " ~ $user_role`.
Contraria o D6 da change anterior: a distinção vai para o registro do
servidor, nunca para a resposta.

**4. Responde `inputerror` (400)** quando a linha do usuário sumiu, com
`"User not found with the provided ID."` — confirma inexistência de conta para
quem tem token velho, onde o certo é um 403 genérico.

**5. Não tem guarda de `user_id > 0`.**

**6. É objeto do template** (`tags = ["xano:quick-start"]`), e um re-push a
substitui. O projeto já pagou esse preço uma vez, ao pôr `id_user` em `tutor`
e não em `user`.

### D4 — Conta sem papel: nega dos dois lados, por construção

`role` é opcional. Criar a linha da conta e esquecer a coluna é o erro de
operação mais provável desta change inteira.

**Do lado da equipe:** `exige_equipe` compara `$conta.role == "admin"`. Vazio,
nulo, `"Admin"`, `"administrador"` e qualquer valor fora do enum caem todos do
mesmo lado — negado — com a mesma mensagem e o mesmo corpo de qualquer outra
recusa.

**Por que a forma da comparação é o que faz isso falhar fechado:**

| Forma | O que faz com papel vazio |
|---|---|
| `== "admin"` | **nega** — e nega também o valor fora do enum |
| `!= "member"` | **permite** — "não é tutor, logo é equipe" |
| `!= null` | **permite** se o vazio for `""`, que é o que o Xano grava |
| `enforce_role` | depende de como o runtime compara — direção errada (D3) |

As duas formas do meio **passariam em revisão**: leem como se estivessem
certas. `!= "member"` é justamente a forma que o **ramo** por papel convida,
porque num ramo o jeito natural de dizer é pela negação — e o desenho que
defendeu o ramo validou essa forma no parser: ela compila limpa.

**A regra que fica para o projeto inteiro:** papel se confere por **igualdade
com o valor esperado**, nunca por negação do outro valor nem por teste de
nulidade.

**Do lado do tutor nada muda, e este é o ponto que vale fixar.** O acesso do
tutor não vem do papel, vem da **posse**: o `join` até `tutor` com
`where = $db.tutor.id_user == $auth.id` não consulta `role` em instante
nenhum. Papel vazio nunca concede nada, nos dois lados, **por razões
independentes**.

**Na tela:** `/auth/me` devolve papel vazio, o roteamento manda `"admin"` para
`/equipe`, `"member"` para `/`, e **qualquer outra coisa para `/` com aviso
explícito** — "sua conta está sem perfil definido; procure a clínica". Hoje
acontece pior: `papel_legivel()` em `petbits/xano.py` devolve "Tutor" para
tudo que não for `"admin"`, a pessoa cai na lista de animais, o filtro de
posse não acha ficha nenhuma e ela lê **"Nenhum animal cadastrado ainda"** — o
sintoma absurdo com que a própria proposta abre reclamando. O aviso explícito
não vaza nada: só é visto por quem já tem a senha da própria conta.

**A auditoria pós-criação não pode ser `role not in ("admin","member")`.** Ela
não pega o erro mais provável de todos, que é criar a conta de equipe com
`"member"` — o outro valor válido do enum, e o que a própria aplicação grava
em todo cadastro. A conferência é **`role != "admin"` entre as contas que
deviam ser de equipe**. Enquanto promover alguém for um gesto fora da
aplicação, a conferência também tem de ser.

### D5 — Duas abas, um caminho só

**A aba não participa da verificação, e mais: ela não é enviada ao backend.**
Nem no corpo, nem na query string, nem em cabeçalho, nem no caminho. Não é
"enviada e ignorada" — enquanto o servidor não souber qual aba foi usada,
nenhuma change futura consegue fazer a resposta depender dela. É a mesma forma
de argumento do D5 da change anterior ("o dono não é entrada, em verbo
nenhum"): a maneira de garantir que um dado não influencia a resposta é ele
não chegar.

O caminho é idêntico nas duas abas, sempre nesta ordem e sempre com estas duas
requisições:

1. `POST /auth/login` — mesma URL, mesmo método, mesmas chaves no corpo, mesma
   ordem, mesmos cabeçalhos. Nada de `POST /auth/login/equipe`.
2. `GET /auth/me` — **sempre**, nas duas abas, mesmo quando a aba escolhida já
   "diz" o papel. É daqui, e só daqui, que sai o destino.

As duas abas são **o mesmo componente e o mesmo manipulador de estado**
(`entrar()` em `auth_state.py`), não dois. Isso não é organização de código: é
o que faz o tempo e o número de requisições serem iguais **por construção**.

**O que especificamente não pode diferir:**

1. A requisição: método, URL, conjunto e ordem das chaves do corpo,
   cabeçalhos.
2. O status HTTP, na recusa e no sucesso.
3. O corpo da recusa, **byte a byte** — mesma string, mesmo `error_type`,
   nenhum campo dizendo de qual aba veio. Nada de "esta conta não é de
   colaborador" ou "use a outra aba".
4. O corpo do sucesso — e ele **não pode conter o papel**. Hoje `auth/login`
   devolve `{authToken, user_id}` e tem de ficar assim. Se o papel entrasse
   ali "para economizar uma requisição", a aba Colaborador poderia recusar sem
   a segunda chamada, e o oráculo volta inteiro.
5. **O tempo de resposta.** É o canal que se perde primeiro. Proibido "se a
   aba for Colaborador, confira o papel antes de aceitar": isso é uma
   requisição a mais numa aba só, cronometrável de fora mesmo com corpos
   idênticos. **Regra geral: nenhuma verificação de papel pode acontecer antes
   da verificação de senha, em endpoint nenhum de entrada.**
6. O número de requisições que a tela dispara: duas, nas duas abas, sempre.
7. O redirecionamento — vem do papel que `/auth/me` devolveu, **nunca da aba**.
8. O destino da recusa e o estado da tela depois dela: mesma aba, mesmo campo
   em foco, mesmos campos limpos.
9. A validação do formulário. Se a aba Colaborador exigisse domínio
   corporativo, o próprio formulário seria o oráculo, antes de qualquer
   requisição sair.
10. Os elementos estáticos e o bloqueio por repetição de tentativas, quando
    existir.
11. **A regra que cobre o que esquecemos de listar:** *nada na resposta —
    status, corpo, tempo, número de chamadas, destino — pode ser função do
    e-mail digitado nem do papel da conta, **antes** de uma senha correta.*
    Depois de uma senha correta, pode: quem tem a credencial já sabe quem é.

**Pode diferir, e deve: o registro no servidor.** Gravar no `event_log` a aba
escolhida ajuda o diagnóstico ("colaborador não consegue entrar" é chamado
real) e não é observável por quem sonda.

**Os dois casos cruzados, com o comportamento exato:**

- **Tutor entra pela aba Colaborador, credenciais corretas.** Entra. 200,
  sessão iniciada, vai para `/` — "Meus animais". **Nenhum erro, nenhum
  aviso, nenhuma menção à aba.** "Esta conta não é da equipe" seria a única
  diferença observável entre as abas — e seria o oráculo de papel inteiro, de
  graça.
- **Colaborador entra pela aba Cliente, credenciais corretas.** Entra e vai
  para `/equipe`, sem aviso: quem tem a senha da conta de equipe não recebe
  informação nova ao saber que ela é de equipe.

**Registro honesto sobre o produto.** Como a aba não muda nada observável, ela
é afordância pura: serve para a clínica dizer "entre pela aba Colaborador".
**A versão mais forte desta decisão seria não ter as abas.** A proposta já
decidiu que elas existem; então o desenho é "duas abas, um caminho só", e isso
precisa estar escrito onde quem for mexer vai ler — porque duas abas que não
fazem nada são uma afirmação falsa na tela, e alguém vai "consertar" isso
fazendo-as fazer algo, que é justamente o vazamento.

**E a tela da equipe forjada?** Quem editar `petbits_papel` para `admin` no
armazenamento local vê o menu da equipe e recebe 403 em cada requisição. A
interface mente, o backend não — já é a regra escrita em `auth_state.py`, e
`exige_equipe` é o que a torna verdadeira do lado novo.

### D6 — Dois irmãos quebram a propriedade por fora

O D5 sustenta a indistinguibilidade **pelo canal da tela de entrada**. Dois
endpoints irmãos a quebram sem tocar nessa tela. Os dois arquivos foram lidos:

**`POST /auth/signup` é um oráculo de uma requisição, sem token.**
E-mail que já existe → 403 com `"An account with this email already exists."`;
e-mail que não existe → 200, conta criada. Sondando e-mails do domínio da
clínica, isso entrega quem tem conta de acesso — e admin é conta `user`.
**Vira tarefa obrigatória despublicá-lo**, não recomendação: o projeto cria
tutor por `POST /tutor/cadastro` e não usa o signup.

*Correção de um desenho que foi atacado e caiu:* o motivo **não** é "ele cria
conta sem papel". O arquivo grava `role: "member"` literal — isso foi
conferido. O motivo é **enumeração de contas de acesso**, e com o motivo certo
ele deixa de ser opinião e vira a mesma família de falha que o D9 da change
anterior registrou no cadastro público.

**`POST /auth/login` tem oráculo de tempo.** `precondition ($user != null)`
vem **antes** de `security.check_password`. E-mail inexistente responde sem
nunca rodar a comparação de hash; e-mail existente com senha errada roda. O
corpo cumpre a spec de `autenticacao`; o relógio não. Isso vaza **existência
de conta**, não o organograma — as duas abas seguem idênticas entre si —, mas
contradiz o invariante 11 do D5, e as abas tornam "este e-mail é da clínica?"
uma pergunta explicitamente interessante.

A correção é um endpoint **próprio**, `PetBits/entrar`, que roda
`security.check_password` **sempre**, inclusive quando a conta não existe,
contra um hash de descarte. Próprio, e não uma edição do `auth/login` do
template, pelo mesmo motivo do item 6 do D3: objeto `xano:quick-start` é
desfeito por um re-push.

**Correção ao próprio desenho, encontrada na aplicação.** O parágrafo acima
estava incompleto, e do jeito mais constrangedor: ele manda escrever um
endpoint novo e **não manda aposentar o velho**. Com `auth/login` continuando
publicado, o oráculo de tempo segue alcançável na URL irmã, com as mesmas
credenciais — e `PetBits/entrar` não conserta absolutamente nada. É palavra
por palavra o argumento que este mesmo D6 usa contra o `auth/signup`
("enquanto esse endpoint responder assim, a propriedade crítica está quebrada
por um irmão"), e ele não foi aplicado ao irmão óbvio. **`auth/login` é
despublicado junto com `auth/signup`**; `auth/me` fica, porque o roteamento
por papel depende dele e ele exige token.

A lição que fica para as próximas changes: **defesa nova sem aposentadoria da
antiga é decoração.** Vale a pena perguntar, para toda defesa, por qual outra
porta a mesma pergunta continua sendo respondida.

**E um terceiro achado, que não é sobre abas:** o `auth/login` do template
inclui `"password"` no `output` e manda `metadata: $user` para o
`log_event` — então **o hash da senha é copiado para `event_log` a cada
entrada**. E `GET /logs/user/my_events` faz `db.query event_log` com
`return = {type: "list"}` e **sem `output`**, devolvendo as linhas cruas. Logo
o dono da conta lê de volta o próprio hash de senha pelos eventos. Não escala
para outra conta (o `where` é por dono), mas é hash exposto ao cliente e dado
sensível em repouso no log.

### D7 — O painel agregado: juntar recursos, não papéis

A forma ingênua — as quatro listas no `on_load` do painel — custa **4
requisições em navegação quente, 5 na carga fria** (o `GET /auth/me` que
`carregar_sessao` dispara quando `sessao_validada` é falso) e **9 consultas ao
banco**. Isso é metade do orçamento da instância numa única abertura de tela.
Dois colaboradores abrindo o painel ao mesmo tempo zeram a janela; um F5
dentro dos 20 segundos derruba o painel **e a tela dos tutores junto**, porque
o limite é por instância. **Rejeitada.**

**Forma adotada: `GET /equipe/painel`, só com contagens.**

| | HTTP | Banco |
|---|---|---|
| Painel, carga fria | 2 de 10 (`auth/me` + painel) | 5 (1 prova + 4 contagens) |
| Painel, navegação quente | 1 | 5 |
| Cada listagem aberta depois | +1 | 2 (1 prova + 1 consulta) |

Explorar as quatro áreas continua custando 5 no total, mas **distribuídas por
cliques** em vez de uma rajada no `on_load`. É a diferença entre caber no
orçamento e estourá-lo.

**Ganho secundário real:** a prova de equipe é **uma** para as quatro
leituras. Não há como uma das quatro ter sido publicada sem prova, porque só
existe uma.

Dois corolários:

- **A prova de papel tem de ser função, nunca requisição.** `function.run`
  roda dentro da pilha e não consome o orçamento de HTTP. No momento em que
  alguém criar um `GET /equipe/sou-equipe` para o Reflex perguntar antes de
  montar o menu, cada tela passa a custar uma requisição a mais — e esse
  endpoint seria, ele próprio, um oráculo de papel chamável com qualquer
  token.
- **O menu da equipe não se desenha perguntando ao backend.**
  `usuario_papel` já está no `rx.LocalStorage` desde a entrada e serve para
  adaptar a tela, nunca para proteger dado.

**O que o painel não deve fazer:** mostrar os quatro contadores *e* as
primeiras linhas de cada lista. Parece barato na tela, custa as 4 requisições
que o resumo existe para evitar, e no caso de `tutor` põe documento e contato
de clientes numa tela de recepção que fica aberta o dia todo.

### D8 — A forma de contar é a provada, não a bonita

O painel conta com `output = ["id"]` + `return = {type: "list"}` + `|count` —
que é o que `tutor_do_token` já usa em produção (fato medido 9: lista nua,
`$x|count`, não `$x.items|count`).

`return = {type: "count"}` **nunca foi exercitado nesta conta**, e é
exatamente a família de construto cujo erro devolve **lista vazia com status
200** (fato medido 5). Um painel que mostra zero colaboradores e zero animais
porque a forma de contagem está errada, sem erro nenhum, seria lido como "a
clínica está vazia", não como bug.

Então: **medir com endpoint descartável antes de usar**, como o projeto mediu
o `0`, o rollback e o `===`. Se funcionar, troca-se; se não, a forma com
`|count` já serve e o limite fica documentado.

**Detalhe:** a contagem de animais é `db.query pet` **sem `join` até
`tutor`**, de propósito — um inner join descartaria em silêncio o animal órfão
(`id_tutor` gravado como 0, fato medido 1), e contagem que esconde o registro
quebrado é pior que contagem nenhuma. É o mesmo motivo pelo qual
`equipe/animais` usa `left` e não `inner` (spec de `animais`: "animal sem
tutor válido aparece para a equipe").

### D9 — A guarda de repositório, e o que ela não alcança

Um script conferindo, para cada `apis/pet_bits/equipe_*.xs`: `auth = "user"`,
`precondition ($auth.id > 0)` e `function.run "PetBits/exige_equipe"` — e a
regra inversa, que nenhum endpoint fora de `equipe_*` chame a prova.

O motivo é o do D2: `colaborador` não tem coluna de dono, logo **não há
`where` para esquecer**. Se a chamada a `exige_equipe` sair da pilha,
`db.query colaborador` devolve a tabela inteira para qualquer conta
autenticada. **O parser aprova o arquivo com e sem a prova.** Reparar na
**ausência** de uma linha é mais difícil do que reparar numa linha errada; a
guarda transforma isso numa pergunta que um script responde.

A guarda tem teste próprio: um arquivo de equipe sem a prova, que ela precisa
acusar. **Ela fecha parcialmente:** endpoint criado pela interface do Xano não
passa pelo repositório. O que pega esse caso é o teste de duas contas (token
de tutor → 403, token de admin → 200) como célula obrigatória de cada
endpoint — espelho do teste de duas contas que a change anterior já exige do
lado do tutor.

### D10 — O que o parser não cobra em colaborador e serviço

As specs pedem recusas que nenhuma declaração de coluna garante. Pelo padrão
do D8 da change anterior, elas moram na pilha, antes da gravação:

- **Função fora do conjunto** (veterinário, tosador, atendente): a coluna é
  `enum`, mas a recusa precisa ser explícita e com mensagem, não um 500 cru.
- **Duração > 0** e **preço >= 0**, na criação **e** na alteração. A spec
  tem cenário próprio para "duração não pode ser zerada na alteração" — e é o
  caso que o `pick` do PATCH torna possível, porque `0` é um valor informado,
  não um campo omitido.
- **Nome e função não vazios após `trim`**, pelo mesmo motivo que
  `pet_update.xs` já guarda: a change anterior encontrou POST aceitando nome
  só de espaços.

A alteração segue o padrão `pick` do `pet_update.xs` — só os campos presentes
no corpo cru são tocados, para que "os campos não mencionados permanecem" seja
estrutural.

### D11 — O que o grupo 1 mediu, e o que mudou por causa disso

**`return = {type: "count"}` funciona.** Conferido contra a forma por lista no
mesmo endpoint: 2 == 2 em `pet`, 3 == 3 em `user` — que tem coluna `enum`, que
era a parte duvidosa. **O D8 fica revisto:** o painel usa `count`, não
`output = ["id"]` + `|count`. Some o risco de carregar quatro listas de id para
a memória só para contar, e o limite que estava registrado em Risks deixa de
existir.

**`security.check_password` com hash vazio lança** — `ERROR_FATAL: Invalid
password syntax.`, HTTP 500. Então a bifurcação que a tarefa 1.3 previa se
resolveu para o lado caro: a entrada de tempo constante do D6 **precisa de um
bcrypt real guardado em constante**, e não de uma string vazia. Um hash
inválido não "falha a comparação": ele derruba a requisição, e derrubar só no
caminho da conta inexistente seria um oráculo melhor do que o que a defesa
veio corrigir.

**E um aviso de método, que vale mais que as duas medições.** A primeira
rodada devolveu **zero em tudo** — a base tinha sido limpa no fim da change
anterior, e eu quase registrei isso como resultado. Zero batendo com zero é
consistente tanto com "`count` funciona" quanto com "`count` falha devolvendo
lista vazia com 200", que é precisamente o modo de falha que a medição existia
para pegar (fato medido 5). **Medição sobre base vazia não mede nada**, e o
construto cujo erro é silencioso é justamente aquele em que o falso verde
passa despercebido. Foi preciso semear e repetir.

## Risks / Trade-offs

**+1 consulta ao banco em toda requisição de equipe, sem exceção.** É o preço
direto de o papel não estar no token, e não é negociável dentro deste desenho:
o endpoint agregado reduz requisições HTTP, não esse custo. Efeito colateral a
registrar: toda chamada de uma sessão de equipe toca a tabela `user`, da qual
o login inteiro depende.

**A superfície de equipe tem uma defesa só.** A do tutor tem duas
independentes (o papel é irrelevante lá, e o `join` de posse recorta a
consulta). Aqui, se `exige_equipe` faltar, a consulta devolve a clínica
inteira para qualquer conta logada. É o que justifica a guarda do D9 e o teste
de duas contas — nenhum dos dois é zelo, os dois são a segunda camada.

**A guarda de repositório não alcança endpoint criado pela interface do
Xano.** Quem criar um endpoint pelo painel está fora de todas as redes, e só o
teste de duas contas pega — se alguém souber que tem de rodá-lo num endpoint
que não está no repositório.

**`GET /equipe/tutores` entrega documento, telefone e endereço de todos os
tutores para qualquer conta `admin`.** É o requisito, mas significa que uma
credencial de equipe comprometida é a base de clientes inteira. Esta change
não prevê registro de acesso por linha nem limite de volume — e o `event_log`
já está pendente de política de retenção desde o D9 da change anterior, e vai
crescer mais com a superfície nova.

**A escrita de equipe não foi desenhada.** O padrão prova + ação do D1 da
change anterior fica mais apertado lá: a consulta-prova da equipe não tem
cláusula de dono nenhuma, então ela vira apenas "existe?". Merece análise
própria, e esta change não a fez — por isso a visão da clínica é só leitura.

**A validação de escrita de animal mora inline em `pet_update.xs`.** Quando a
equipe ganhar escrita de animal, ela será copiada e passarão a existir duas
cópias que podem divergir. A saída é extrair para função, como `tutor_do_token`
já foi. **Esta change não faz isso, e a dívida vence na próxima.**

**Conta rebaixada de equipe para cliente com token ainda válido:** os
endpoints negam na hora (o papel vem do banco), mas o navegador continua com
`usuario_papel = "admin"` no LocalStorage e com o menu da equipe montado, e a
pessoa vê uma tela cheia de 403. Não é falha de segurança; é uma tela quebrada
que ninguém especificou.

**A aba descartada em silêncio gera chamado de suporte.** Um tutor que escolhe
deliberadamente "Colaborador" não recebe explicação nenhuma. É a decisão certa
de privacidade. Aceito e registrado, não resolvido.

**A conta de equipe criada sem papel, ou com `member` por engano, fica
trancada nas duas áreas com mensagem genérica** — e é exatamente assim que o
primeiro admin da clínica vai nascer. O comportamento está certo; a
experiência não. Precisa de distinção no registro do servidor e de uma linha
na documentação de operação.

**`colaborador` não liga a `user`,** seguindo a proposta — então nada no
sistema diz qual conta de equipe corresponde a qual pessoa. O registro só terá
`user_id`, e numa auditoria de "quem alterou este serviço" isso não responde à
pergunta. Consequência aceita do escopo, não defeito. (É por isso que
`exige_equipe` devolve o id da conta: pelo menos há o que registrar.)

**O `GET /equipe/painel` tende a virar endpoint-Deus:** cada widget novo
acrescenta uma consulta e nada o limita. Ele existe por causa do limite de
10/20s — é concessão à plataforma, não boa arquitetura, e merece estar escrito
como tal.

~~**`|count` sobre quatro consultas carrega quatro listas de id para a
memória.**~~ **Resolvido pela medição** — o painel usa `return =
{type: "count"}` (D11).

**Que o valor de um `enum?` vazio seja `""` e não nulo é inferência por
analogia** (o `0` do vínculo, o `"default": ""` observado no schema de um
campo `date`), **não medição**. A igualdade contra `"admin"` está correta sob
as duas hipóteses, então a decisão não depende disso — mas a ênfase sobre
`!= null` no D4 depende.

**O que o grupo 1 mediu está no D11; o que ele não cobriu continua suposto.**
A contagem e o `check_password` com hash vazio foram medidos. **Não** foram:
o comportamento de `db.patch` sobre a tabela `servico` com valor zero
informado (a guarda está escrita, mas a interação `pick` + zero só se prova
exercitando), e o custo real do painel em requisições, que a tarefa 6.6 mede
na aba de rede. Até lá, os números do D7 são aritmética, não observação.

## Migration Plan

Nada a migrar em dado existente: `colaborador` e `servico` nascem vazias, e
nenhuma coluna de tabela existente muda.

A ordem das tarefas é escolhida pelo risco:

1. **Medir** o que o desenho pressupõe (contagem, hash de descarte), antes de
   escrever endpoint definitivo.
2. **`exige_equipe` e as tabelas** — a função antes de qualquer endpoint que a
   use, para que não exista janela em que um endpoint de equipe esteja no ar
   sem prova.
3. **Endpoints de equipe**, cada um com seu teste de duas contas.
4. **A guarda de repositório**, com o teste dela.
5. **Os irmãos do D6** (`auth/signup`, entrada de tempo constante, hash no
   log) — mexem em autenticação, que é o que derruba todo mundo se der errado,
   então vão depois de a superfície nova estar provada.
6. **Reflex**: abas, roteamento por papel, área da equipe.

O primeiro admin é criado à mão no painel do Xano, com a conferência do D4
rodada **depois** da criação.
