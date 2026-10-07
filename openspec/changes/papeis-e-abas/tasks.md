# Tasks

## 1. O papel novo no banco

- [x] 1.1 Acrescentar `"staff"` ao enum de `user.role` em `tables/898256_user.xs`; verificar pelo schema publicado que os três valores saíram — e **só o enum neste passo**, porque gravar o valor novo depende dele estar no ar

## 2. As duas provas

- [x] 2.1 Alterar `functions/pet_bits/exige_equipe.xs` para aceitar `admin` **ou** `staff`, mantendo a forma por **igualdade** contra cada literal; verificar lendo o arquivo que não virou `!= "member"` — papel vazio, com erro de digitação ou futuro tem de continuar caindo do lado negado
- [x] 2.2 Escrever `functions/pet_bits/exige_gerencia.xs`, irmã da anterior, aceitando só `admin`; verificar no parser e conferir que ela devolve o **id da conta**, nunca o papel, pelo mesmo motivo da irmã
- [x] 2.3 Confirmar que as recusas das duas saem **iguais entre si** — mesmo `error_type`, mesma mensagem; verificar que uma conta `staff` recusada pela gerência recebe o mesmo corpo que um tutor recusado pela equipe, para não revelar em que degrau a conta está
- [x] 2.4 Publicar as duas funções e exercitar por três tokens (tutor, staff, admin); verificar a matriz 3×2 — **feito com os endpoints de verdade** (tarefa 4.3) em vez de um descartável, que é evidência mais forte: exercita o caminho que vai para produção, e não um irmão dele

## 3. A escrita de colaborador passa à gerência

- [x] 3.1 Trocar a prova em `apis/pet_bits/equipe_colaborador_create.xs` e `equipe_colaborador_update.xs` para `exige_gerencia`; verificar que **só** esses dois mudaram, com `git diff --stat`
- [x] 3.2 Confirmar que os outros nove endpoints de equipe continuam com `exige_equipe`; verificar que `equipe_colaborador_get` e `_list` **não** foram trocados — ler colaborador continua sendo de toda a equipe
- [x] 3.3 Ensinar a guarda de repositório: todo `equipe_*.xs` chama **uma das duas** provas, e `exige_gerencia` aparece **exatamente** nos dois arquivos de escrita de colaborador; verificar as duas pontas, inclusive um arquivo que troque uma prova pela outra — é a troca que ninguém nota lendo o diff

## 4. A migração das contas

- [x] 4.1 Rebaixar para `staff` as contas de Thiago, Letícia, Bianca e Otávio; verificar que Carla, Patricia, Rafael e Sandra continuam `admin`
- [x] 4.2 Rodar a conferência do D4 — `role == "admin"` entre quem **não** deveria ser gerência; verificar que ela acusaria uma conta esquecida, testando com uma descartável antes de apagá-la. A conferência antiga (`!= "admin"`) rodada hoje não acusa nada, e é por isso que ela precisa ser a nova
- [x] 4.3 Testar a matriz de verdade com token real: `staff` lê colaborador (200) e não escreve (403); `admin` lê e escreve (200); tutor não alcança nada (403); verificar os seis casos

## 5. A aba passa a valer

- [x] 5.1 Comparar, no Reflex, o papel devolvido por `/auth/me` com a aba escolhida, **depois** da entrada; verificar que a sessão é descartada quando não combina e que a pessoa volta à tela com a orientação
- [x] 5.2 Confirmar que a aba **continua não sendo enviada** ao servidor; verificar na aba de rede que `POST /entrar` e `GET /auth/me` são idênticos nas duas abas, na mesma ordem
- [x] 5.3 **Medir** que a propriedade crítica não quebrou: com credencial **errada**, comparar status, corpo e tempo nas duas abas; verificar que seguem indistinguíveis — esta é a tarefa que decide se a change pode entrar
- [x] 5.4 Conta sem papel conhecido é recusada nas duas abas, com a orientação de procurar a clínica; verificar com uma conta descartável de papel vazio, e apagá-la depois

## 6. A interface por nível

- [x] 6.1 Esconder os controles de criar e alterar colaborador para quem não é gerência; verificar com conta `staff` que a lista aparece e os botões não
- [x] 6.2 Confirmar que esconder é **só** conveniência; verificar forjando o papel no armazenamento local que os botões voltam e que cada operação volta 403
- [x] 6.3 O olho da senha nos campos de senha da entrada e do cadastro; verificar que começa oculto e que sair da tela e voltar não deixa a senha visível

## 7. O que a revisão da change anterior deixou

- [x] 7.1 Corrigir `petbits/pages/inicio.py`: a tela do tutor mostra o erro **e** o spinner ao mesmo tempo, para sempre, porque "carregando" é o caso padrão de tudo que sobra. É o mesmo defeito que a área da equipe já corrigiu, e o tutor ficou para trás; verificar provocando um erro de carga que só o erro aparece
- [x] 7.2 Trocar o seletor de função por `rx.select.root` com rótulos legíveis; verificar que o diálogo mostra "Clínico geral" onde hoje mostra `clinico_geral`, batendo com o que o cartão ao lado já exibe
- [x] 7.3 Atualizar os quatro lugares que ainda dizem que `funcao` tem três valores — `tasks.md` da change anterior (tarefa 2.1, **marcada como cumprida** contra um critério que hoje reprovaria o schema certo), `design.md` D10, os dois comentários de `tables/colaborador.xs` e `docs/domain-model.md`; verificar com `grep` que não sobrou nenhum

## 8. Verificação de integração

- [x] 8.1 Percurso da gerência: entrar pela aba Colaborador, cadastrar e editar colaborador, abrir as quatro áreas; verificar que tudo funciona
- [x] 8.2 Percurso da equipe comum: entrar, ver colaboradores sem poder editar, mexer no catálogo de serviços, consultar tutores e animais; verificar que só a escrita de colaborador recusa
- [x] 8.3 Percurso do tutor: entrar pela aba Cliente e ver os animais; verificar que nada mudou
- [x] 8.4 Os dois cruzamentos de aba, com senha **correta**: equipe pela aba Cliente e tutor pela aba Colaborador; verificar que os dois são recusados com orientação e sem sessão aberta
- [x] 8.5 Rodar `openspec validate --strict`, o validador de XanoScript e a guarda; verificar que os três passam antes de arquivar


## O que a aplicação achou, e que o desenho não previa

**`redirecionar_se_logado` mandava todo mundo para `/`.** Uma conta de equipe
que voltasse à tela de entrada já logada caía na área do tutor e lia
"Nenhum animal cadastrado ainda" — exatamente o sintoma absurdo com que a
change anterior abriu reclamando, e que ela corrigiu **só** no caminho da
entrada. Este caminho ficou para trás, e só apareceu quando a gerência foi
testada de verdade na tela. Agora ele usa `rota_do_papel`, como o resto.

Fica a pergunta que vale para as próximas: *quais são os outros lugares que
decidem para onde alguém vai?* Corrigir o caminho principal e esquecer os
laterais foi o mesmo erro duas changes seguidas.

**A medição da 5.3, que decidia se a change podia entrar:** com senha errada,
as duas abas produzem **uma requisição, a mesma** (`POST /entrar`), e a mesma
mensagem. A aba nem é consultada — o `except XanoError` retorna na linha 16 do
método e a comparação de aba está na 40. Vale por construção, não por cuidado
de quem revisa.
