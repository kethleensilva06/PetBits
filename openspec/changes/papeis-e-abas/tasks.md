# Tasks

## 1. O papel novo no banco

- [ ] 1.1 Acrescentar `"staff"` ao enum de `user.role` em `tables/898256_user.xs`; verificar pelo schema publicado que os três valores saíram — e **só o enum neste passo**, porque gravar o valor novo depende dele estar no ar

## 2. As duas provas

- [ ] 2.1 Alterar `functions/pet_bits/exige_equipe.xs` para aceitar `admin` **ou** `staff`, mantendo a forma por **igualdade** contra cada literal; verificar lendo o arquivo que não virou `!= "member"` — papel vazio, com erro de digitação ou futuro tem de continuar caindo do lado negado
- [ ] 2.2 Escrever `functions/pet_bits/exige_gerencia.xs`, irmã da anterior, aceitando só `admin`; verificar no parser e conferir que ela devolve o **id da conta**, nunca o papel, pelo mesmo motivo da irmã
- [ ] 2.3 Confirmar que as recusas das duas saem **iguais entre si** — mesmo `error_type`, mesma mensagem; verificar que uma conta `staff` recusada pela gerência recebe o mesmo corpo que um tutor recusado pela equipe, para não revelar em que degrau a conta está
- [ ] 2.4 Publicar as duas funções e exercitar com um endpoint descartável por três tokens (tutor, staff, admin); verificar a matriz 3×2 e remover o descartável

## 3. A escrita de colaborador passa à gerência

- [ ] 3.1 Trocar a prova em `apis/pet_bits/equipe_colaborador_create.xs` e `equipe_colaborador_update.xs` para `exige_gerencia`; verificar que **só** esses dois mudaram, com `git diff --stat`
- [ ] 3.2 Confirmar que os outros nove endpoints de equipe continuam com `exige_equipe`; verificar que `equipe_colaborador_get` e `_list` **não** foram trocados — ler colaborador continua sendo de toda a equipe
- [ ] 3.3 Ensinar a guarda de repositório: todo `equipe_*.xs` chama **uma das duas** provas, e `exige_gerencia` aparece **exatamente** nos dois arquivos de escrita de colaborador; verificar as duas pontas, inclusive um arquivo que troque uma prova pela outra — é a troca que ninguém nota lendo o diff

## 4. A migração das contas

- [ ] 4.1 Rebaixar para `staff` as contas de Thiago, Letícia, Bianca e Otávio; verificar que Carla, Patricia, Rafael e Sandra continuam `admin`
- [ ] 4.2 Rodar a conferência do D4 — `role == "admin"` entre quem **não** deveria ser gerência; verificar que ela acusaria uma conta esquecida, testando com uma descartável antes de apagá-la. A conferência antiga (`!= "admin"`) rodada hoje não acusa nada, e é por isso que ela precisa ser a nova
- [ ] 4.3 Testar a matriz de verdade com token real: `staff` lê colaborador (200) e não escreve (403); `admin` lê e escreve (200); tutor não alcança nada (403); verificar os seis casos

## 5. A aba passa a valer

- [ ] 5.1 Comparar, no Reflex, o papel devolvido por `/auth/me` com a aba escolhida, **depois** da entrada; verificar que a sessão é descartada quando não combina e que a pessoa volta à tela com a orientação
- [ ] 5.2 Confirmar que a aba **continua não sendo enviada** ao servidor; verificar na aba de rede que `POST /entrar` e `GET /auth/me` são idênticos nas duas abas, na mesma ordem
- [ ] 5.3 **Medir** que a propriedade crítica não quebrou: com credencial **errada**, comparar status, corpo e tempo nas duas abas; verificar que seguem indistinguíveis — esta é a tarefa que decide se a change pode entrar
- [ ] 5.4 Conta sem papel conhecido é recusada nas duas abas, com a orientação de procurar a clínica; verificar com uma conta descartável de papel vazio, e apagá-la depois

## 6. A interface por nível

- [ ] 6.1 Esconder os controles de criar e alterar colaborador para quem não é gerência; verificar com conta `staff` que a lista aparece e os botões não
- [ ] 6.2 Confirmar que esconder é **só** conveniência; verificar forjando o papel no armazenamento local que os botões voltam e que cada operação volta 403
- [ ] 6.3 O olho da senha nos campos de senha da entrada e do cadastro; verificar que começa oculto e que sair da tela e voltar não deixa a senha visível

## 7. O que a revisão da change anterior deixou

- [ ] 7.1 Corrigir `petbits/pages/inicio.py`: a tela do tutor mostra o erro **e** o spinner ao mesmo tempo, para sempre, porque "carregando" é o caso padrão de tudo que sobra. É o mesmo defeito que a área da equipe já corrigiu, e o tutor ficou para trás; verificar provocando um erro de carga que só o erro aparece
- [ ] 7.2 Trocar o seletor de função por `rx.select.root` com rótulos legíveis; verificar que o diálogo mostra "Clínico geral" onde hoje mostra `clinico_geral`, batendo com o que o cartão ao lado já exibe
- [ ] 7.3 Atualizar os quatro lugares que ainda dizem que `funcao` tem três valores — `tasks.md` da change anterior (tarefa 2.1, **marcada como cumprida** contra um critério que hoje reprovaria o schema certo), `design.md` D10, os dois comentários de `tables/colaborador.xs` e `docs/domain-model.md`; verificar com `grep` que não sobrou nenhum

## 8. Verificação de integração

- [ ] 8.1 Percurso da gerência: entrar pela aba Colaborador, cadastrar e editar colaborador, abrir as quatro áreas; verificar que tudo funciona
- [ ] 8.2 Percurso da equipe comum: entrar, ver colaboradores sem poder editar, mexer no catálogo de serviços, consultar tutores e animais; verificar que só a escrita de colaborador recusa
- [ ] 8.3 Percurso do tutor: entrar pela aba Cliente e ver os animais; verificar que nada mudou
- [ ] 8.4 Os dois cruzamentos de aba, com senha **correta**: equipe pela aba Cliente e tutor pela aba Colaborador; verificar que os dois são recusados com orientação e sem sessão aberta
- [ ] 8.5 Rodar `openspec validate --strict`, o validador de XanoScript e a guarda; verificar que os três passam antes de arquivar
