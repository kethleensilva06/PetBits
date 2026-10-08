# Tasks

## 1. Cadastro de tutor de balcão

- [ ] 1.1 Escrever `apis/pet_bits/equipe_tutor_create.xs`, rota `equipe/tutores` POST, com a abertura padrão e `exige_equipe` — **não** gerência; verificar lendo o arquivo que a prova está antes de qualquer `db.*`
- [ ] 1.2 Normalizar o documento na pilha, como o cadastro público faz, e conferir com `db.has` **antes** do `db.add`; verificar que `123.456.789-01` e `12345678901` são recusados um contra o outro — sem isso o índice único é contornável por pontuação, e a porta de balcão vira a fácil
- [ ] 1.3 Recusar documento repetido com mensagem **explícita**, ao contrário do cadastro público; verificar que a resposta diz que o documento já está cadastrado, e que isso é coerente porque quem pergunta aqui é uma atendente autenticada que já tem a lista inteira a um clique
- [ ] 1.4 Recusar nome ou documento vazios depois de `trim`; verificar com os dois casos
- [ ] 1.5 Confirmar que o tutor criado **não** recebe conta: nenhuma linha em `user`, e `id_user` fica no valor que o Xano grava para vínculo omitido; verificar na tabela depois de criar
- [ ] 1.6 Testar com token de equipe comum (aceita), de gerência (aceita) e de tutor (403); verificar os três

## 2. Cadastro de animal pela clínica

- [ ] 2.1 Escrever `apis/pet_bits/equipe_animal_create.xs`, rota `equipe/animais` POST, com `exige_equipe`; verificar que a prova está antes de qualquer `db.*`
- [ ] 2.2 Conferir o `id_tutor` **contra o banco** antes de gravar, e gravar pelo id que a **consulta** devolveu, nunca pelo do input; verificar lendo o arquivo — é a forma que faz copiar este arquivo não perder a parte que importa
- [ ] 2.3 Recusar `id_tutor` ausente, zerado e inexistente; verificar os três e confirmar que nenhum animal órfão foi criado
- [ ] 2.4 Recusar nome ou espécie vazios depois de `trim`; verificar com os dois casos
- [ ] 2.5 Confirmar que o animal criado pela clínica **aparece para o tutor dele**; verificar com o token do tutor que ele veio na lista — é o que prova que o vínculo foi gravado de verdade, e não só que o endpoint devolveu 200
- [ ] 2.6 Escrever no topo dos **dois** arquivos de criação de animal (o do tutor e o da equipe) em qual lado da regra de dono cada um está, e por quê; verificar que os dois comentários existem — é defesa fraca contra copiar um como modelo do outro, e está registrada como fraca
- [ ] 2.7 Testar com token de equipe comum, de gerência e de tutor; verificar os três

## 3. As telas

- [ ] 3.1 Formulário de novo tutor na tela de tutores, aberto a toda a equipe; verificar que a lista recarrega com o novo tutor depois de salvar
- [ ] 3.2 Avisar, no formulário, que o tutor cadastrado **não terá acesso ao aplicativo** enquanto a clínica não ligar uma conta; verificar que o aviso aparece antes de salvar, e não depois — descobrir isso depois é o que esta change existe para evitar
- [ ] 3.3 Formulário de novo animal na tela de animais, com **escolha do tutor responsável**; verificar que a lista de tutores vem da mesma carga que a tela já faz, sem requisição a mais
- [ ] 3.4 Confirmar que as duas telas deixaram de ser só leitura **sem** ganhar editar nem excluir; verificar que não há botão de alterar em nenhuma das duas — esta change acrescenta só a criação

## 4. Verificação de integração

- [ ] 4.1 Percurso de balcão completo: entrar como equipe comum, cadastrar um tutor, cadastrar um animal para ele, e vê-lo na lista da clínica; verificar cada passo
- [ ] 4.2 Confirmar que o animal cadastrado pela clínica aparece **na área do tutor**, entrando com a conta dele; verificar com um tutor que tenha conta
- [ ] 4.3 Confirmar que o caminho do tutor não mudou: `POST /pet` com `id_tutor` de outra pessoa continua criando para o dono da credencial; verificar que o cenário "dono forjado na criação" segue valendo
- [ ] 4.4 Rodar `openspec validate --strict`, o validador de XanoScript e a guarda; verificar que os três passam
