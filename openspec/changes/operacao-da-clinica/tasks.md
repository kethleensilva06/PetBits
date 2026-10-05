# Tasks

## 1. Medir o que o desenho pressupõe

Antes de escrever qualquer endpoint definitivo. As duas premissas abaixo o
parser aceita, mas o motor do Xano nunca foi exercitado nesta conta — e a
primeira decide a forma do painel inteiro (design.md, D8).

- [ ] 1.1 Medir `return = {type: "count"}` num endpoint descartável sobre `pet`, com linhas na base; verificar que o número devolvido bate com a contagem real — se devolver lista vazia com 200, ou qualquer coisa que não seja o número, registrar no design e manter a forma `output = ["id"] + |count|`
- [ ] 1.2 Medir `|count` sobre uma consulta cujo `output` traz só `["id"]` de uma tabela com coluna `enum`; verificar que o número bate, porque é a forma que o painel usa em `user` e `colaborador`
- [ ] 1.3 Medir o que `security.check_password` faz com `hash_password` vazio: endpoint descartável que chama com `""`; verificar se devolve falso ou lança — se lançar, o hash de descarte da tarefa 8.2 tem de ser um bcrypt real guardado em constante, e isso vai para o design
- [ ] 1.4 Remover os endpoints descartáveis; verificar pela listagem de endpoints do grupo PetBits que nenhum sobrou

## 2. Tabelas novas

- [ ] 2.1 Criar `tables/colaborador.xs` com `nome` (text), `funcao` (enum: veterinario, tosador, atendente), `telefone?`, `email?`, `data_entrada?` (timestamp — **nunca** `date`, pelo fato medido 7) e `ativo` (bool, default true); verificar pelo schema publicado que `funcao` saiu como enum com exatamente os três valores
- [ ] 2.2 Criar `tables/servico.xs` com `nome` (text), `descricao?`, `preco` (decimal) e `duracao_minutos` (int); verificar pelo schema publicado que nenhuma das duas últimas é opcional
- [ ] 2.3 Confirmar que **nenhuma** das duas tabelas tem coluna apontando para `user` ou `tutor`; verificar lendo os dois arquivos — é o que a proposta decidiu e o que o D2 pressupõe ao dizer que não há `where` de dono para esquecer

## 3. A prova de equipe

A função vem **antes** de qualquer endpoint que a use, para que não exista
janela em que um endpoint de equipe esteja publicado sem prova.

- [ ] 3.1 Escrever `functions/pet_bits/exige_equipe.xs`: `precondition ($input.user_id > 0)`, `db.get user` com `output = ["id", "role"]`, `precondition ($conta != null)`, `precondition ($conta.role == "admin")`, e `response = $conta.id`; verificar no parser (`node scripts/validar_xanoscript.mjs`) antes de publicar
- [ ] 3.2 Confirmar que as três recusas saem com `error_type = "accessdenied"` e **a mesma mensagem**; verificar lendo o arquivo — quem sonda não pode aprender em que estado a conta alheia está (D2)
- [ ] 3.3 Confirmar que a função devolve o **id**, nunca o papel; verificar lendo a linha do `response` — se devolvesse o papel, o primeiro `if` por papel nasceria no endpoint chamador (D1, D2)
- [ ] 3.4 Publicar a função e exercitá-la por um endpoint descartável com token de tutor e com token de admin; verificar 403 no primeiro e 200 no segundo, e remover o descartável em seguida

## 4. Colaboradores

- [ ] 4.1 `apis/pet_bits/equipe_colaborador_list.xs`: `auth = "user"`, `precondition ($auth.id > 0)`, `function.run "PetBits/exige_equipe"`, `precondition ($id_conta > 0)`, e só então `db.query colaborador` com `output` explícito e `sort` por nome; verificar que a prova está **antes** da consulta, lendo o arquivo
- [ ] 4.2 `equipe_colaborador_get.xs` com a mesma abertura; verificar que identificador inexistente devolve `notfound`, e não lista vazia
- [ ] 4.3 `equipe_colaborador_create.xs`: a mesma abertura, mais `precondition` de nome não vazio após `trim` e de função dentro do conjunto; verificar com três requisições — nome só de espaços recusado, função `"recepcionista"` recusada com mensagem (não 500 cru), e cadastro só com nome e função aceito
- [ ] 4.4 `equipe_colaborador_update.xs` no padrão `pick` do `pet_update.xs`: `util.get_raw_input`, `$dados = $input|pick:($corpo_cru|keys)|unset:"colaborador_id"`, guarda contra esvaziar nome e função, `db.patch` com `field_value`; verificar alterando só o telefone e conferindo que nome e função ficaram como estavam
- [ ] 4.5 Testar os quatro com token de tutor; verificar 403 em cada um, e que o corpo não traz nome, contato nem função de ninguém

## 5. Serviços

- [ ] 5.1 `equipe_servico_list.xs` e `equipe_servico_get.xs` com a mesma abertura das tarefas 4.1 e 4.2; verificar que a prova está antes da consulta nos dois
- [ ] 5.2 `equipe_servico_create.xs` com `precondition` de nome não vazio, `duracao_minutos > 0` e `preco >= 0`; verificar com quatro requisições — sem nome recusado, duração `0` recusada, preço `-10` recusado, e serviço com preço `0` **aceito** (serviço gratuito é válido, spec de `servicos`)
- [ ] 5.3 `equipe_servico_update.xs` no padrão `pick`, com as mesmas guardas de duração e preço aplicadas **também** na alteração; verificar enviando `duracao_minutos: 0` num serviço existente e conferindo que foi recusado **e** que a duração anterior permanece — é o cenário que o `pick` torna possível, porque `0` é valor informado, não campo omitido (D10)
- [ ] 5.4 Testar os quatro com token de tutor; verificar 403 em cada um e que o catálogo permanece inalterado depois das tentativas

## 6. A visão da clínica

- [ ] 6.1 `equipe_tutor_list.xs` com a abertura padrão e `output` explícito; verificar que um tutor sem conta de acesso (`id_user = 0`) **aparece** na lista — é o cenário "tutor de balcão aparece" da spec de `tutores`, e o que distingue esta consulta da do tutor
- [ ] 6.2 `equipe_animal_list.xs` com `join` até `tutor` do tipo **`left`**, não `inner`, e `output` incluindo o nome do tutor; verificar com um animal órfão (`id_tutor = 0`) na base que ele **aparece** para a equipe — com `inner` ele sumiria em silêncio, e a spec de `animais` exige o contrário
- [ ] 6.3 Confirmar que `pet_list.xs` **não** foi tocado; verificar com `git diff` que o arquivo do tutor segue idêntico, e com token de tutor que ele continua devolvendo só os animais dele
- [ ] 6.4 `equipe_painel.xs`: uma prova de equipe e quatro contagens (colaboradores, serviços, tutores, animais), na forma que a tarefa 1.1 determinou; verificar que os quatro números batem com as listas, e que a contagem de animais **não** tem `join` até `tutor`, para não esconder o órfão (D8)
- [ ] 6.5 Confirmar que o painel devolve **só contagens**, nenhuma linha de nenhuma lista; verificar lendo o `response` — primeiras linhas no painel custam as quatro requisições que ele existe para evitar, e no caso de tutor põem documento e contato numa tela de recepção (D7)
- [ ] 6.6 Medir o custo real da abertura do painel: contar as requisições HTTP na aba de rede do navegador, em carga fria e em navegação quente; verificar que são 2 e 1, e anotar o número no design se divergir

## 7. As redes

- [ ] 7.1 Escrever `scripts/verificar_equipe.py` (ou `.mjs`) que, para cada `apis/pet_bits/equipe_*.xs`, exige `auth = "user"`, `precondition ($auth.id > 0)` e `function.run "PetBits/exige_equipe"`; verificar que ele passa limpo no repositório real
- [ ] 7.2 Dar à guarda a regra inversa: nenhum arquivo **fora** de `equipe_*` chama `exige_equipe`; verificar que ela passa limpo e que não confunde arquivo de função com endpoint
- [ ] 7.3 Testar a guarda contra um caso negativo: copiar um endpoint de equipe sem a linha da prova, num arquivo temporário; verificar que ela **acusa**, e apagar o arquivo depois — guarda que nunca falhou não é guarda
- [ ] 7.4 Montar a tabela de teste de duas contas, uma linha por endpoint de equipe: token de tutor → 403, token de admin → 200; verificar que **todos** os endpoints de equipe têm as duas células preenchidas, e registrar o resultado no `tasks.md` ou num arquivo de evidência
- [ ] 7.5 Criar a conta de equipe à mão no painel do Xano e rodar a conferência do D4 — `role != "admin"` entre as contas que deviam ser de equipe; verificar que a conferência acusaria uma conta criada com `"member"` por engano, testando com uma conta descartável antes de apagá-la

## 8. Os irmãos da autenticação

Mexem no que derruba todo mundo se der errado, então vêm depois de a
superfície nova estar provada (design.md, Migration Plan).

- [ ] 8.1 Despublicar `POST /auth/signup`; verificar com `curl` que ele deixou de responder, e que `POST /tutor/cadastro` continua criando tutor normalmente — é o endpoint que o projeto de fato usa (D6)
- [ ] 8.2 Escrever `apis/pet_bits/entrar.xs`, endpoint próprio de entrada que roda `security.check_password` **sempre**, inclusive quando a conta não existe, contra o hash de descarte que a tarefa 1.3 determinou; verificar que ele devolve `{authToken, user_id}` e **não** devolve o papel
- [ ] 8.3 Medir o tempo de resposta de `PetBits/entrar` com e-mail inexistente e com e-mail existente + senha errada, dez vezes cada; verificar que as distribuições se sobrepõem — se não se sobrepuserem, o desenho não cumpriu o que prometeu e volta para o design (D6)
- [ ] 8.4 Confirmar que a recusa dos dois casos sai com o mesmo status, o mesmo `error_type` e a mesma mensagem; verificar comparando os dois corpos byte a byte
- [ ] 8.5 Tirar `"password"` do `output` do `db.get user` da entrada e parar de passar `$user` cru como `metadata` para `log_event`, passando um objeto montado com id, e-mail e ação; verificar que uma entrada nova **não** grava hash no `event_log`
- [ ] 8.6 Pôr `output` explícito em `GET /logs/user/my_events`; verificar que a resposta deixou de trazer o campo de metadata cru — hoje o dono da conta lê de volta o próprio hash de senha pelos eventos (D6)
- [ ] 8.7 Corrigir `apis/pet_bits/me_tutor.xs`: acrescentar `precondition ($auth.id > 0)` como primeira instrução e trocar `db.get tutor` por `db.query tutor` com `where = $db.tutor.id_user == $auth.id`; verificar que a ficha certa continua voltando, e que é o único endpoint privado do grupo que estava sem a guarda

## 9. Aplicação Reflex

- [ ] 9.1 Abas *Cliente* e *Colaborador* na tela de entrada, usando **o mesmo componente e o mesmo manipulador de estado**; verificar lendo `entrar()` em `auth_state.py` que não existe ramo por aba dentro dele (D5)
- [ ] 9.2 Confirmar que a aba **não é enviada** ao backend: nem no corpo, nem na query, nem em cabeçalho, nem no caminho; verificar na aba de rede do navegador que as duas requisições são idênticas nas duas abas
- [ ] 9.3 Roteamento por papel depois do `GET /auth/me`: `"admin"` → `/equipe`, `"member"` → `/`, **qualquer outra coisa** → `/` com aviso explícito de conta sem perfil; verificar com uma conta de papel vazio que o aviso aparece, em vez de "Nenhum animal cadastrado ainda" (D4)
- [ ] 9.4 Corrigir `papel_legivel()` em `petbits/xano.py`, que hoje devolve "Tutor" para tudo que não for `"admin"`; verificar que papel vazio passa a ser tratado como desconhecido, não como tutor
- [ ] 9.5 Área da equipe com navegação própria e `EquipeState` novo; verificar que o menu se desenha a partir de `usuario_papel` do LocalStorage, **sem** nenhuma requisição ao backend para perguntar o papel (D7)
- [ ] 9.6 Acrescentar o `EquipeState` à limpeza do `sair()` em `auth_state.py`; verificar entrando como equipe, saindo e entrando como tutor, que nenhum dado da clínica aparece — a change anterior deixou registrado que essa lista cresce e que esquecê-la é silencioso
- [ ] 9.7 Telas de colaboradores e de serviços, com os formulários de criar e alterar; verificar que o CRUD das duas funciona de ponta a ponta com conta de equipe
- [ ] 9.8 Telas de consulta a tutores e animais da clínica, **sem** botões de criar ou alterar; verificar que a ausência deles é o que comunica "só leitura", porque a escrita de equipe não foi desenhada
- [ ] 9.9 Painel da equipe consumindo `GET /equipe/painel`, com as listas carregadas **sob demanda**, ao clicar; verificar na aba de rede que abrir o painel dispara uma requisição, não quatro
- [ ] 9.10 Tratar 429 em todas as telas com mensagem clara e recuo antes de repetir, começando pelo painel; verificar provocando o limite com F5 repetido que aparece "muitas requisições, tente de novo em instantes", e não o erro cru que a spec de `autenticacao` proíbe
- [ ] 9.11 Guarda de rota da área da equipe como **retorno antecipado** dentro do loader, não `rx.redirect` no `on_load`; verificar com token de tutor que acessar `/equipe` direto não dispara requisição nenhuma de dado da clínica

## 10. Verificação de integração

- [ ] 10.1 Percurso do colaborador: entrar pela aba Colaborador, abrir o painel, cadastrar um colaborador, cadastrar um serviço, consultar tutores e animais; verificar que cada passo funciona e anotar o total de requisições do percurso
- [ ] 10.2 Percurso do tutor: entrar pela aba Cliente, ver os animais dele, cadastrar um animal; verificar que nada mudou em relação à change anterior
- [ ] 10.3 **Teste cruzado das abas:** entrar com a conta de tutor pela aba *Colaborador*; verificar que a sessão inicia normalmente e a pessoa vai para "Meus animais", **sem nenhum aviso sobre a aba** (D5)
- [ ] 10.4 Entrar com a conta de equipe pela aba *Cliente*; verificar que vai para `/equipe`, também sem aviso
- [ ] 10.5 **Teste do oráculo:** com credencial errada, gravar as duas requisições nas duas abas; verificar que status, corpo, número de requisições e tempo são indistinguíveis — é a prova da propriedade crítica do D5
- [ ] 10.6 **Teste do papel forjado:** editar `petbits_papel` para `admin` no LocalStorage com uma conta de tutor; verificar que o menu da equipe aparece (a interface mente) e que **cada** requisição da clínica volta 403 com corpo vazio de dado (o backend não mente)
- [ ] 10.7 Rodar `openspec validate --strict` e a guarda da tarefa 7.1; verificar que os dois passam limpos antes de arquivar
