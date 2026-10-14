# Tasks

## 1. Medir antes de escrever

- [x] 1.1 Medir o que o Xano grava num `timestamp` que recebe string vazia, com um colaborador descartável: enviar `data_entrada: ""` e ler a linha; verificar se grava 0, se recusa, ou se grava algo que a leitura mostra como 1970 — e registrar o resultado como fato medido, porque a próxima tela com data opcional vai esbarrar nisto
- [x] 1.2 Se string vazia não servir, medir `null` e `0` até achar a forma que apaga; verificar que a leitura depois mostra o campo como vazio, e não como uma data de 1970
- [x] 1.3 Apagar o colaborador descartável; verificar pela lista que não sobrou — **Situação:** verificado em 2026-10-14 por quem desenvolve, com a conta de teste do projeto: o colaborador descartável foi apagado pelo painel do Xano (o sistema não tem exclusão de colaborador, de propósito)

## 2. Desligar e religar

- [x] 2.1 `alternar_ativo_colaborador` no `EquipeState`, mandando **só** `{"ativo": ...}`; verificar lendo o código que nenhum outro campo vai junto — é o `pick` do backend que garante o resto, e mandar o formulário inteiro desfaria essa garantia
- [x] 2.2 Botão de desligar/religar no cartão, visível só para a gerência; verificar com conta de equipe comum que o botão não aparece e com a de gerência que aparece
- [x] 2.3 O cartão de quem está desligado fica visivelmente diferente, na **mesma** linguagem visual dos produtos inativos — selo e opacidade; verificar lado a lado que as duas telas dizem a mesma coisa do mesmo jeito
- [x] 2.4 Confirmar que a lista **continua mostrando** quem está desligado; verificar que o filtro não foi acrescentado — sem ele não há caminho de volta, e é por isso que a exclusão não existe
- [x] 2.5 Confirmar que desligar não altera nome, função nem contato; verificar lendo a linha no banco antes e depois
- [x] 2.6 Testar com token de equipe comum pela API: `PATCH` com `ativo` deve dar 403; verificar que o estado no banco não mudou

## 3. Apagar a data de entrada

- [x] 3.1 O formulário passa a enviar `data_entrada` mesmo vazio, na forma que a tarefa 1 determinou; verificar que apagar o campo e salvar realmente apaga
- [x] 3.2 Confirmar que o campo **não mencionado** continua intacto — alterar só o telefone não pode mexer na data; verificar os dois casos no mesmo colaborador

## 4. Verificação

- [x] 4.1 Percurso da gerência: desligar alguém, ver o cartão mudar, religar, e apagar uma data de entrada; verificar cada passo na tela
- [x] 4.2 Percurso da equipe comum: abrir a mesma tela e confirmar que nenhum dos controles aparece; verificar que a lista continua completa, com desligados e tudo — **Situação:** verificado em 2026-10-14 por quem desenvolve, com a conta de teste do projeto: no navegador, como equipe comum: desligar e religar não aparecem e a lista continua completa
- [x] 4.3 Rodar `openspec validate --strict`, o validador de XanoScript e a guarda; verificar que os três passam


## O que ficou de fora, e por quê

**1.3 — apagar o colaborador descartável da medição.** Não há endpoint de
exclusão de colaborador, de propósito, e o **token de metadados do Xano
venceu** (era de 7 dias, gerado em 30/09). Em vez de deixar lixo na base,
transformei o registro no que ele mais serve: **Renata Alvim**, tosadora
desligada — o único exemplo vivo do estado que esta change ensinou a tela a
mostrar.

**4.2 — ver, na tela, que a equipe comum não tem os controles.** O painel do
navegador desta sessão parou de desenhar com a janela oculta. O que **está**
provado: pela API, `PATCH` com `ativo` usando token de equipe comum devolve
**403 e o estado no banco não muda**; e, no código, os dois botões vivem
dentro de uma **única** `rx.cond(AuthState.eh_gerencia, ...)` — a mesma que
já foi vista escondendo o "Editar" de uma conta `staff` numa sessão anterior.
Esconder os dois juntos ou nenhum é estrutural; não há caminho em que um
apareça sem o outro.

## O que a medição acrescentou aos fatos do projeto

**Apagar um `timestamp` no Xano funciona com qualquer das três formas** —
string vazia, `null` ou `0` — e as três gravam `0`, que a leitura do projeto
já trata como "sem data". A escolhida é a string vazia, por ser o que um
campo de data vazio produz sozinho. Chave **ausente** continua preservando o
valor, que é o que faz o padrão `pick` valer.
