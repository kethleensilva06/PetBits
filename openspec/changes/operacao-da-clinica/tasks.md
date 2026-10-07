# Tasks

## 1. Medir o que o desenho pressupõe

Antes de escrever qualquer endpoint definitivo. As duas premissas abaixo o
parser aceita, mas o motor do Xano nunca foi exercitado nesta conta — e a
primeira decide a forma do painel inteiro (design.md, D8).

- [x] 1.1 Medir `return = {type: "count"}` num endpoint descartável sobre `pet`, com linhas na base; verificar que o número devolvido bate com a contagem real — se devolver lista vazia com 200, ou qualquer coisa que não seja o número, registrar no design e manter a forma `output = ["id"] + |count|`
- [x] 1.2 Medir `|count` sobre uma consulta cujo `output` traz só `["id"]` de uma tabela com coluna `enum`; verificar que o número bate, porque é a forma que o painel usa em `user` e `colaborador`
- [x] 1.3 Medir o que `security.check_password` faz com `hash_password` vazio: endpoint descartável que chama com `""`; verificar se devolve falso ou lança — se lançar, o hash de descarte da tarefa 8.2 tem de ser um bcrypt real guardado em constante, e isso vai para o design
- [x] 1.4 Remover os endpoints descartáveis; verificar pela listagem de endpoints do grupo PetBits que nenhum sobrou

**O que o grupo 1 mediu** (detalhe em design.md, D11):
`return = {type: "count"}` **funciona** — conferido contra a forma por lista,
2 == 2 em `pet` e 3 == 3 em `user`, que tem coluna `enum`. O painel usa a
forma barata. E `security.check_password` com hash vazio **lança**
`ERROR_FATAL: Invalid password syntax.` — a entrada de tempo constante precisa
de um bcrypt real em constante.

A primeira rodada da medição deu **zero em tudo**, porque a base tinha sido
limpa no fim da change anterior. Zero batendo com zero é consistente tanto com
"`count` funciona" quanto com "`count` falha devolvendo vazio" — que é
exatamente o modo de falha que a medição existe para pegar. Foi preciso semear
a base e repetir. Fica como aviso para as próximas: **medição sobre base vazia
não mede nada.**

## 2. Tabelas novas

- [x] 2.1 Criar `tables/colaborador.xs` com `nome` (text), `funcao` (enum: veterinario, tosador, atendente), `telefone?`, `email?`, `data_entrada?` (timestamp — **nunca** `date`, pelo fato medido 7) e `ativo` (bool, default true); verificar pelo schema publicado que `funcao` saiu como enum com exatamente os três valores
- [x] 2.2 Criar `tables/servico.xs` com `nome` (text), `descricao?`, `preco` (decimal) e `duracao_minutos` (int); verificar pelo schema publicado que nenhuma das duas últimas é opcional
- [x] 2.3 Confirmar que **nenhuma** das duas tabelas tem coluna apontando para `user` ou `tutor`; verificar lendo os dois arquivos — é o que a proposta decidiu e o que o D2 pressupõe ao dizer que não há `where` de dono para esquecer

## 3. A prova de equipe

A função vem **antes** de qualquer endpoint que a use, para que não exista
janela em que um endpoint de equipe esteja publicado sem prova.

- [x] 3.1 Escrever `functions/pet_bits/exige_equipe.xs`: `precondition ($input.user_id > 0)`, `db.get user` com `output = ["id", "role"]`, `precondition ($conta != null)`, `precondition ($conta.role == "admin")`, e `response = $conta.id`; verificar no parser (`node scripts/validar_xanoscript.mjs`) antes de publicar
- [x] 3.2 Confirmar que as três recusas saem com `error_type = "accessdenied"` e **a mesma mensagem**; verificar lendo o arquivo — quem sonda não pode aprender em que estado a conta alheia está (D2)
- [x] 3.3 Confirmar que a função devolve o **id**, nunca o papel; verificar lendo a linha do `response` — se devolvesse o papel, o primeiro `if` por papel nasceria no endpoint chamador (D1, D2)
- [x] 3.4 Publicar a função e exercitá-la por um endpoint descartável com token de tutor e com token de admin; verificar 403 no primeiro e 200 no segundo, e remover o descartável em seguida

## 4. Colaboradores

- [x] 4.1 `apis/pet_bits/equipe_colaborador_list.xs`: `auth = "user"`, `precondition ($auth.id > 0)`, `function.run "PetBits/exige_equipe"`, `precondition ($id_conta > 0)`, e só então `db.query colaborador` com `output` explícito e `sort` por nome; verificar que a prova está **antes** da consulta, lendo o arquivo
- [x] 4.2 `equipe_colaborador_get.xs` com a mesma abertura; verificar que identificador inexistente devolve `notfound`, e não lista vazia
- [x] 4.3 `equipe_colaborador_create.xs`: a mesma abertura, mais `precondition` de nome não vazio após `trim` e de função dentro do conjunto; verificar com três requisições — nome só de espaços recusado, função `"recepcionista"` recusada com mensagem (não 500 cru), e cadastro só com nome e função aceito
- [x] 4.4 `equipe_colaborador_update.xs` no padrão `pick` do `pet_update.xs`: `util.get_raw_input`, `$dados = $input|pick:($corpo_cru|keys)|unset:"colaborador_id"`, guarda contra esvaziar nome e função, `db.patch` com `field_value`; verificar alterando só o telefone e conferindo que nome e função ficaram como estavam
- [x] 4.5 Testar os quatro com token de tutor; verificar 403 em cada um, e que o corpo não traz nome, contato nem função de ninguém

## 5. Serviços

- [x] 5.1 `equipe_servico_list.xs` e `equipe_servico_get.xs` com a mesma abertura das tarefas 4.1 e 4.2; verificar que a prova está antes da consulta nos dois
- [x] 5.2 `equipe_servico_create.xs` com `precondition` de nome não vazio, `duracao_minutos > 0` e `preco >= 0`; verificar com quatro requisições — sem nome recusado, duração `0` recusada, preço `-10` recusado, e serviço com preço `0` **aceito** (serviço gratuito é válido, spec de `servicos`)
- [x] 5.3 `equipe_servico_update.xs` no padrão `pick`, com as mesmas guardas de duração e preço aplicadas **também** na alteração; verificar enviando `duracao_minutos: 0` num serviço existente e conferindo que foi recusado **e** que a duração anterior permanece — é o cenário que o `pick` torna possível, porque `0` é valor informado, não campo omitido (D10)
- [x] 5.4 Testar os quatro com token de tutor; verificar 403 em cada um e que o catálogo permanece inalterado depois das tentativas

## 6. A visão da clínica

- [x] 6.1 `equipe_tutor_list.xs` com a abertura padrão e `output` explícito; verificar que um tutor sem conta de acesso (`id_user = 0`) **aparece** na lista — é o cenário "tutor de balcão aparece" da spec de `tutores`, e o que distingue esta consulta da do tutor
- [x] 6.2 `equipe_animal_list.xs` com `join` até `tutor` do tipo **`left`**, não `inner`, e `output` incluindo o nome do tutor; verificar com um animal órfão (`id_tutor = 0`) na base que ele **aparece** para a equipe — com `inner` ele sumiria em silêncio, e a spec de `animais` exige o contrário
- [x] 6.3 Confirmar que `pet_list.xs` **não** foi tocado; verificar com `git diff` que o arquivo do tutor segue idêntico, e com token de tutor que ele continua devolvendo só os animais dele
- [x] 6.4 `equipe_painel.xs`: uma prova de equipe e quatro contagens (colaboradores, serviços, tutores, animais), na forma que a tarefa 1.1 determinou; verificar que os quatro números batem com as listas, e que a contagem de animais **não** tem `join` até `tutor`, para não esconder o órfão (D8)
- [x] 6.5 Confirmar que o painel devolve **só contagens**, nenhuma linha de nenhuma lista; verificar lendo o `response` — primeiras linhas no painel custam as quatro requisições que ele existe para evitar, e no caso de tutor põem documento e contato numa tela de recepção (D7)
- [x] 6.6 Medir o custo real da abertura do painel: contar as requisições HTTP na aba de rede do navegador, em carga fria e em navegação quente; verificar que são 2 e 1, e anotar o número no design se divergir

## 7. As redes

- [x] 7.1 Escrever `scripts/verificar_equipe.py` (ou `.mjs`) que, para cada `apis/pet_bits/equipe_*.xs`, exige `auth = "user"`, `precondition ($auth.id > 0)` e `function.run "PetBits/exige_equipe"`; verificar que ele passa limpo no repositório real
- [x] 7.2 Dar à guarda a regra inversa: nenhum arquivo **fora** de `equipe_*` chama `exige_equipe`; verificar que ela passa limpo e que não confunde arquivo de função com endpoint
- [x] 7.3 Testar a guarda contra um caso negativo: copiar um endpoint de equipe sem a linha da prova, num arquivo temporário; verificar que ela **acusa**, e apagar o arquivo depois — guarda que nunca falhou não é guarda
- [x] 7.4 Montar a tabela de teste de duas contas, uma linha por endpoint de equipe: token de tutor → 403, token de admin → 200; verificar que **todos** os endpoints de equipe têm as duas células preenchidas, e registrar o resultado no `tasks.md` ou num arquivo de evidência
- [x] 7.5 Criar a conta de equipe à mão no painel do Xano e rodar a conferência do D4 — `role != "admin"` entre as contas que deviam ser de equipe; verificar que a conferência acusaria uma conta criada com `"member"` por engano, testando com uma conta descartável antes de apagá-la

## 8. Os irmãos da autenticação

Mexem no que derruba todo mundo se der errado, então vêm depois de a
superfície nova estar provada (design.md, Migration Plan).

- [x] 8.1 Despublicar `POST /auth/signup`; verificar com `curl` que ele deixou de responder, e que `POST /tutor/cadastro` continua criando tutor normalmente — é o endpoint que o projeto de fato usa (D6)
- [x] 8.1b Despublicar **também** `POST /auth/login`, junto com o signup; verificar com `curl` que ele parou de responder e que `POST /entrar` atende no lugar — sem isto o `entrar.xs` da tarefa seguinte não conserta nada, porque o oráculo de tempo continua alcançável na URL irmã com as mesmas credenciais. `auth/me` **fica**: o roteamento por papel depende dele e ele exige token
- [x] 8.2 Escrever `apis/pet_bits/entrar.xs`, endpoint próprio de entrada que roda `security.check_password` **sempre**, inclusive quando a conta não existe, contra o hash de descarte que a tarefa 1.3 determinou; verificar que ele devolve `{authToken, user_id}` e **não** devolve o papel
- [x] 8.3 Medir o tempo de resposta de `PetBits/entrar` com e-mail inexistente e com e-mail existente + senha errada, dez vezes cada; verificar que as distribuições se sobrepõem — se não se sobrepuserem, o desenho não cumpriu o que prometeu e volta para o design (D6)
- [x] 8.4 Confirmar que a recusa dos dois casos sai com o mesmo status, o mesmo `error_type` e a mesma mensagem; verificar comparando os dois corpos byte a byte
- [x] 8.5 Tirar `"password"` do `output` do `db.get user` da entrada e parar de passar `$user` cru como `metadata` para `log_event`, passando um objeto montado com id, e-mail e ação; verificar que uma entrada nova **não** grava hash no `event_log`
- [x] 8.6 Pôr `output` explícito em `GET /logs/user/my_events`; verificar que a resposta deixou de trazer o campo de metadata cru — hoje o dono da conta lê de volta o próprio hash de senha pelos eventos (D6)
- [x] 8.7 Corrigir `apis/pet_bits/me_tutor.xs`: acrescentar `precondition ($auth.id > 0)` como primeira instrução e trocar `db.get tutor` por `db.query tutor` com `where = $db.tutor.id_user == $auth.id`; verificar que a ficha certa continua voltando, e que é o único endpoint privado do grupo que estava sem a guarda

## 9. Aplicação Reflex

- [x] 9.1 Abas *Cliente* e *Colaborador* na tela de entrada, usando **o mesmo componente e o mesmo manipulador de estado**; verificar lendo `entrar()` em `auth_state.py` que não existe ramo por aba dentro dele (D5)
- [x] 9.2 Confirmar que a aba **não é enviada** ao backend: nem no corpo, nem na query, nem em cabeçalho, nem no caminho; verificar na aba de rede do navegador que as duas requisições são idênticas nas duas abas
- [x] 9.3 Roteamento por papel depois do `GET /auth/me`: `"admin"` → `/equipe`, `"member"` → `/`, **qualquer outra coisa** → `/` com aviso explícito de conta sem perfil; verificar com uma conta de papel vazio que o aviso aparece, em vez de "Nenhum animal cadastrado ainda" (D4)
- [x] 9.4 Corrigir `papel_legivel()` em `petbits/xano.py`, que hoje devolve "Tutor" para tudo que não for `"admin"`; verificar que papel vazio passa a ser tratado como desconhecido, não como tutor
- [x] 9.5 Área da equipe com navegação própria e `EquipeState` novo; verificar que o menu se desenha a partir de `usuario_papel` do LocalStorage, **sem** nenhuma requisição ao backend para perguntar o papel (D7)
- [x] 9.6 Acrescentar o `EquipeState` à limpeza do `sair()` em `auth_state.py`; verificar entrando como equipe, saindo e entrando como tutor, que nenhum dado da clínica aparece — a change anterior deixou registrado que essa lista cresce e que esquecê-la é silencioso
- [x] 9.7 Telas de colaboradores e de serviços, com os formulários de criar e alterar; verificar que o CRUD das duas funciona de ponta a ponta com conta de equipe
- [x] 9.8 Telas de consulta a tutores e animais da clínica, **sem** botões de criar ou alterar; verificar que a ausência deles é o que comunica "só leitura", porque a escrita de equipe não foi desenhada
- [x] 9.9 Painel da equipe consumindo `GET /equipe/painel`, com as listas carregadas **sob demanda**, ao clicar; verificar na aba de rede que abrir o painel dispara uma requisição, não quatro
- [x] 9.10 Tratar 429 em todas as telas com mensagem clara e recuo antes de repetir, começando pelo painel; verificar provocando o limite com F5 repetido que aparece "muitas requisições, tente de novo em instantes", e não o erro cru que a spec de `autenticacao` proíbe
- [x] 9.11 Guarda de rota da área da equipe como **retorno antecipado** dentro do loader, não `rx.redirect` no `on_load`; verificar com token de tutor que acessar `/equipe` direto não dispara requisição nenhuma de dado da clínica

## 10. Verificação de integração

- [x] 10.1 Percurso do colaborador: entrar pela aba Colaborador, abrir o painel, cadastrar um colaborador, cadastrar um serviço, consultar tutores e animais; verificar que cada passo funciona e anotar o total de requisições do percurso
- [x] 10.2 Percurso do tutor: entrar pela aba Cliente, ver os animais dele, cadastrar um animal; verificar que nada mudou em relação à change anterior
- [x] 10.3 **Teste cruzado das abas:** entrar com a conta de tutor pela aba *Colaborador*; verificar que a sessão inicia normalmente e a pessoa vai para "Meus animais", **sem nenhum aviso sobre a aba** (D5)
- [x] 10.4 Entrar com a conta de equipe pela aba *Cliente*; verificar que vai para `/equipe`, também sem aviso
- [x] 10.5 **Teste do oráculo:** com credencial errada, gravar as duas requisições nas duas abas; verificar que status, corpo, número de requisições e tempo são indistinguíveis — é a prova da propriedade crítica do D5
- [x] 10.6 **Teste do papel forjado:** editar `petbits_papel` para `admin` no LocalStorage com uma conta de tutor; verificar que o menu da equipe aparece (a interface mente) e que **cada** requisição da clínica volta 403 com corpo vazio de dado (o backend não mente)
- [x] 10.7 Rodar `openspec validate --strict` e a guarda da tarefa 7.1; verificar que os dois passam limpos antes de arquivar


## O que as medições do fim acharam

**6.6 — custo do painel, medido.** Instrumentando a camada HTTP do Reflex (o
painel de rede do navegador não enxerga: as chamadas ao Xano saem do backend
Python):

| | requisições |
|---|---|
| Entrar | 2 — `POST /entrar` + `GET /auth/me` |
| Painel, carga fria (aba nova) | **2 de 10** |
| Painel, navegação quente | 1 |
| Cada área aberta depois | +1, **sem `auth/me` repetido** |
| As quatro áreas | 5 no total, distribuídas por clique |

A forma ingênua gastaria as mesmas 5 **numa rajada só**, no carregamento do
painel. O gancho de medição ficou em `petbits/xano.py`, desligado por padrão —
liga com a variável de ambiente `PETBITS_MEDIR` apontando para um arquivo.

**8.6 — `my_events` fechado e conferido.** A resposta agora traz apenas
`id`, `created_at` e `action`. Conferido com uma conta real: nem `metadata`
nem `password` aparecem no corpo.

Fechar a **leitura** resolveu mais do que a tarefa pedia. Além do `auth/login`
e do `auth/signup` já despublicados, outros dois endpoints do template
continuam no ar gravando o objeto `$user` cru no log — `reset/magic-link-login`
e `reset/update_password`. Nenhum deles serve o dado de volta agora.

## 11. O que a revisão adversarial achou

Um bloqueio, e ele estava publicado desde antes desta change.

- [x] 11.1 Despublicar `GET /reset/request-reset-link`; verificar com `curl` sem credencial que ele parou de responder — era um oráculo de existência de conta **por status**, numa requisição GET, e enquanto esteve no ar o `entrar.xs` da tarefa 8.2 não tinha efeito prático nenhum
- [x] 11.2 Despublicar `POST /message/send_welcome_email`; verificar que parou de responder — era enumeração de id de conta, pública, e os ids são sequenciais
- [x] 11.3 Despublicar `POST /reset/magic-link-login`; verificar que parou de responder — público, grava `$user` cru no log, e sem o endpoint de pedir o link não tem uso
- [x] 11.4 Conferir que `auth/me` e `reset/update_password` continuam no ar **com** `auth = "user"`, e que o percurso de tutor, de equipe e de gerente continua funcionando depois das três remoções
- [x] 11.5 Registrar no design a forma correta da pergunta: não "qual é o irmão desta defesa", e sim "liste todo endpoint sem `auth = \"user\"` e diga que pergunta cada um responde a quem não tem credencial"

## O que fica registrado como pendente

**Os hashes já gravados continuam na tabela `event_log`.** Nada os serve mais,
mas eles estão lá, em repouso. Apagá-los é a conversa de retenção do
`event_log` que a change anterior já deixou pendente (D9) — e que agora tem um
motivo a mais. Não foi feito aqui porque apagar dado da base é decisão de
quem é dono dela, não da change.

**`my_events` é objeto do template** (`xano:quick-start`). Um re-push do
template substitui o arquivo e o vazamento volta, em silêncio. Foi por isso
que a entrada nova nasceu como endpoint próprio; aqui não havia essa escolha,
porque o endpoint já existia e é o único que serve esta leitura.
