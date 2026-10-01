# Tasks

## 1. Registro de tutor no Xano

- [x] 1.1 Escrever `tables/tutor.xs` com nome e documento obrigatórios, contato opcional e a coluna de vínculo opcional com `user` (D2); verificar rodando o parser oficial do XanoScript sobre o arquivo e obtendo zero erros
- [x] 1.2 Empurrar a tabela e medir o que o Xano grava na coluna de vínculo quando ela é omitida — criar dois tutores sem vínculo e ler os valores crus; verificar que os dois existem e anotar no design (seção D3) se o valor é nulo ou um padrão do tipo
- [x] 1.3 Declarar o índice único sobre o documento e, conforme o resultado de 1.2, o índice do vínculo; verificar que gravar documento repetido é recusado e que dois tutores sem vínculo coexistem

## 2. Cadastro e ficha própria

- [x] 2.1 Escrever o endpoint `POST /tutor/cadastro` na ordem do D4 — conferir e-mail, conferir documento, criar a conta, criar o tutor, devolver o token; verificar com o parser oficial
- [x] 2.2 Empurrar o endpoint e exercitar o caminho feliz; verificar por leitura direta das tabelas que a conta e a ficha existem e estão vinculadas entre si
- [x] 2.3 Exercitar a recusa por e-mail já cadastrado; verificar que a resposta informa o motivo e que nenhum registro novo foi criado
- [x] 2.4 Exercitar a recusa por documento já cadastrado; verificar que **nenhuma conta de acesso ficou criada** — é o cenário "recusa não deixa conta órfã"
- [x] 2.5 Enviar um papel diferente no corpo do cadastro; verificar que a conta nasce mesmo assim como `member`
- [x] 2.6 Escrever e empurrar `GET /me/tutor`; verificar que com token devolve a ficha do próprio usuário, que sem token é recusado, e que uma conta sem ficha recebe resposta vazia em vez de erro cru
- [x] 2.7 Verificar se `transaction` do XanoScript faz rollback real, forçando um erro depois da primeira gravação e conferindo se ela sobreviveu; se fizer, envolver as duas gravações do cadastro e registrar a decisão no design

## 3. Cliente HTTP da aplicação

- [x] 3.1 Instalar no `.venv` uma biblioteca HTTP assíncrona (D8) e registrá-la em `requirements.txt`; verificar que o import funciona e que a versão aparece no arquivo
- [x] 3.2 Escrever o módulo cliente com os dois base URLs, token como argumento nomeado obrigatório (D7) e hierarquia de erro que separa credencial inválida de falha de comunicação; verificar chamando o login com senha errada e conferindo que o tipo de erro é o de credencial, não o de rede
- [x] 3.3 Registrar no próprio módulo o mapeamento de papéis do D9 (`member` é tutor, `admin` é equipe) e concentrar a tradução num só ponto; verificar que nenhuma outra parte do código compara com as strings cruas

## 4. Sessão

- [ ] 4.1 Escrever o State de sessão guardando token e perfil no armazenamento local do navegador, com a marca de validação fora dele (D5); verificar os três cenários da spec: recarregar a página, abrir outra aba e reiniciar o servidor de aplicação
- [ ] 4.2 Implementar sair; verificar que o armazenamento local fica vazio, que a pessoa volta à entrada e que os campos do formulário estão limpos
- [ ] 4.3 Tratar credencial expirada separadamente de falha de comunicação; verificar substituindo o token guardado por um valor inválido (deve cair na entrada com aviso de sessão expirada) e depois deixando o backend inacessível (a sessão deve **permanecer** ativa)

## 5. Telas e rotas

- [ ] 5.1 Construir a tela de cadastro com os campos da spec; verificar que um cadastro completo leva à tela pós-login já autenticado
- [ ] 5.2 Construir a tela de entrada; verificar que senha errada e e-mail inexistente produzem **a mesma** mensagem, sem permitir distinguir os casos
- [ ] 5.3 Construir a tela pós-login que cumprimenta pelo nome; verificar que exibe o nome de quem entrou
- [ ] 5.4 Implementar a guarda com retorno antecipado dentro do carregamento (D6); verificar que um visitante em rota privada vai para a entrada **e** que nenhuma requisição daquela rota chega ao backend
- [ ] 5.5 Registrar as rotas na aplicação; verificar que cada endereço abre a tela correta e que a aplicação sobe sem erro de compilação
- [ ] 5.6 Descrever o primeiro acesso no `README.md` — cadastrar-se e entrar; verificar seguindo o texto num navegador sem sessão e chegando à tela pós-login

## 6. Verificação de integração

- [ ] 6.1 Percorrer no navegador todos os cenários das duas specs de ponta a ponta; verificar que cada cenário se comporta como escrito e anotar qualquer divergência
- [x] 6.2 Conferir por requisição crua, fora da interface, que os endpoints privados recusam sem credencial e que adulterar o papel no armazenamento local não concede acesso nenhum
- [x] 6.3 Contar as requisições ao Xano ao entrar e ao se cadastrar; verificar que nenhuma das duas operações passa de duas requisições
