# Tasks

## 1. Medir o que o desenho pressupõe

Antes de escrever qualquer endpoint definitivo. As três premissas abaixo o
parser aceita, mas o motor do Xano nunca foi exercitado nesta conta — e a
abordagem inteira depende da primeira.

- [x] 1.1 Medir se `$db.<tabela_juntada>.<coluna>` no `where` de topo funciona em runtime: endpoint descartável com `join` até `tutor` e `where` sobre a coluna da tabela juntada; verificar que ele devolve só as linhas do dono, com duas fichas de tutor na base — se não funcionar, o desenho muda e a change volta ao design
- [x] 1.2 Medir se `lock = true` numa `db.query` dentro de `db.transaction` segura a linha até o commit; verificar com duas requisições concorrentes e anotar o resultado no design
- [x] 1.3 Medir se uma variável criada dentro do `stack` de `db.transaction` é visível no `response` fora dele; verificar chamando o endpoint descartável e, se não for, registrar no design qual plano B será usado
- [x] 1.4 Remover os endpoints descartáveis das medições; verificar pela listagem de endpoints do grupo que nenhum sobrou

## 2. Tabela de animais

- [x] 2.1 Escrever `tables/pet.xs` com nome e espécie obrigatórios, demais campos opcionais, `id_tutor` ligado a `tutor`, **nenhuma coluna com índice único** (D8) e índices btree em `id_tutor` e composto `(id_tutor, nome)` para cobrir a ordenação; verificar com o parser oficial
- [x] 2.2 Empurrar a tabela e conferir que ela existe com as colunas e índices declarados; verificar lendo o schema pela API de metadados
- [x] 2.3 Registrar no design a escolha de identificador sequencial como decisão consciente, com o que ela vaza por inferência; verificar que a seção existe no design.md

## 3. Resolver o tutor de quem escreve

- [x] 3.1 Escrever a função reutilizável que resolve o tutor a partir do `$auth.id`, com `return list` e guarda de ambiguidade `== 1` (D4), falhando alto para 0 e para 2 ou mais; verificar com o parser oficial
- [x] 3.2 Empurrar e exercitar os três casos: conta com uma ficha devolve o identificador dela; conta sem ficha é recusada com mensagem sobre a própria conta; verificar criando temporariamente uma segunda ficha na mesma conta que o caso ambíguo também é recusado, e remover a ficha extra depois

## 4. Listagem e leitura por identificador

- [x] 4.1 Escrever `GET /pet` com o padrão de leitura do D1 — join inner até `tutor`, `where` com `===`, `output` explícito sem `id_tutor`, `totals: false`, e `precondition ($auth.id > 0)` no topo; verificar com o parser oficial
- [x] 4.2 Escrever `GET /pet/{pet_id}` com o mesmo padrão e `return single`; verificar com o parser oficial
- [x] 4.3 Empurrar os dois e exercitar com **duas contas reais**: cada tutor vê só os seus; a conta B pede o animal da conta A e recebe "não encontrado", não 200 nem "sem permissão"
- [x] 4.4 Verificar que um identificador inexistente devolve **exatamente** a mesma resposta (status, corpo e mensagem) que o animal alheio — comparar as duas respostas byte a byte
- [x] 4.5 Verificar o conjunto **exato** de chaves da resposta (igualdade, não "contém"), confirmando que documento, telefone, e-mail e endereço do tutor não aparecem, e que `id_tutor` também não (D8)
- [x] 4.6 Verificar que conta sem ficha de tutor recebe lista vazia, e não erro

## 5. Criar e editar

- [x] 5.1 Escrever `POST /pet` com colunas declaradas uma a uma (sem `dblink`), dono vindo só da função do grupo 3, e `precondition` de dono maior que zero antes do `db.add` (D3, D5); verificar com o parser oficial
- [x] 5.2 Escrever `PATCH /pet/{pet_id}` com as três instruções do D1 dentro de `db.transaction` — prova com `lock` e `output`, `precondition` de não encontrado, e `db.patch` por `$meu.id`; verificar com o parser oficial
- [x] 5.3 Empurrar os dois e exercitar o caminho feliz: criar um animal e vê-lo na listagem do dono; editar e conferir que ele continua na listagem
- [x] 5.4 Verificar que `id_tutor` enviado no corpo do POST é ignorado e que o animal nasce do tutor da credencial
- [x] 5.5 Verificar que `id_tutor` enviado no corpo do PATCH não transfere o animal — nem para outra conta, nem de uma conta para a própria
- [x] 5.6 Verificar que a conta B editando o animal da conta A recebe "não encontrado" e que o animal permanece inalterado
- [x] 5.7 Verificar que uma edição não apaga raça, peso e observações que não foram mencionados — é dado clínico, e perdê-lo por omissão é o pior defeito desta change (D8/D4 do dossiê)
- [x] 5.8 Verificar que conta sem ficha de tutor recebe recusa explícita sobre a própria conta ao tentar criar, e que nenhum animal é gravado

## 6. Corrigir o vazamento do cadastro público

- [x] 6.1 Alterar `apis/pet_bits/tutor_cadastro.xs` para mensagem genérica única em e-mail e em documento duplicados, com a distinção indo para o registro do servidor (D9); verificar com o parser oficial
- [x] 6.2 Republicar e verificar que as duas recusas devolvem resposta idêntica, sem permitir deduzir qual dado já existia
- [x] 6.3 Verificar que o motivo específico continua recuperável no servidor, para diagnóstico
- [x] 6.4 Verificar que o cenário "recusa não deixa conta órfã" da change anterior continua valendo depois da alteração

## 7. Aplicação Reflex

- [x] 7.1 Acrescentar as operações de animal ao cliente HTTP, com token obrigatório por chamada; verificar que uma chamada sem token falha na hora, e não com requisição anônima
- [x] 7.2 Escrever o State da tela de animais, carregando a lista pela guarda de sessão existente; verificar que sem sessão nenhuma requisição ao Xano sai
- [x] 7.3 Construir a tela de animais com a lista e o formulário de cadastro; verificar cadastrando um animal e vendo-o aparecer
- [x] 7.4 Permitir editar um animal, enviando o registro completo que a tela já tem em mãos (D4 do dossiê — evita apagar campo por omissão); verificar editando só o nome e conferindo que peso e observações sobrevivem
- [x] 7.5 Trocar o cartão de boas-vindas da tela inicial pela lista de animais; verificar que um tutor sem animais vê um convite a cadastrar, não uma tela vazia ou um erro
- [x] 7.6 Registrar a tela de animais no `README.md`, dentro do primeiro acesso; verificar seguindo o texto num navegador sem sessão

## 8. Verificação de integração

- [ ] 8.1 Percorrer no navegador todos os cenários das duas specs de ponta a ponta, com duas contas; verificar que cada cenário se comporta como escrito e anotar qualquer divergência
- [x] 8.2 Conferir por requisição crua que as quatro operações de animal recusam sem credencial e com credencial forjada
- [x] 8.3 Verificar que uma expressão enviada como busca ou ordenação não altera o filtro de dono, e que página zero ou negativa é recusada sem erro interno
- [x] 8.4 Contar as requisições ao Xano ao abrir a tela de animais; verificar que não passa de duas
- [ ] 8.5 Remover todos os dados de teste criados e confirmar que a base ficou no estado anterior
