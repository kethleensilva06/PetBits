# Proposal

## Why

O sistema já sabe quem entra, mas ainda não sabe cuidar de nada. O tutor
autenticado encontra uma tela que o cumprimenta pelo nome e mais nada — não há
sequer o registro do animal que o levou à clínica.

O Animal é o conceito em torno do qual todo o resto se organiza
(`docs/domain-model.md`): consultas, agendamentos e histórico clínico são
dele, não do tutor. Sem ele, nenhuma das changes seguintes tem sujeito.

Esta change também responde, pela primeira vez, a pergunta que o sistema
inteiro vai repetir: **como o backend prova que um dado é de quem está
pedindo?** O padrão decidido aqui é o que as changes de agendamento e de
histórico clínico vão reusar. É por isso que ela vem antes delas, e não
depois.

## What Changes

- O tutor **cadastra** um animal informando nome, espécie, raça, data de
  nascimento, peso e observações.
- O tutor **vê a lista** dos seus animais, e somente dos seus.
- O tutor **edita** os dados de um animal seu.
- O tutor **não consegue** ver nem alterar o animal de outro tutor, nem pela
  interface nem por requisição direta à API.
- O tutor **não escolhe** de quem é o animal: o dono sai do servidor.
- A tela pós-login deixa de ser um cartão de boas-vindas e passa a mostrar os
  animais do tutor — vira a casa dele.

### Fora do escopo

Agendamento, histórico clínico, catálogo de serviços, cadastro de
colaboradores, área da equipe e petshop. Identidade visual.

**Excluir animal** fica de fora: apagar um animal deixaria agendamentos e
atendimentos futuros apontando para o vazio, e a decisão sobre o que fazer com
o histórico dele pertence à change que criar esse histórico. Por ora um animal
cadastrado permanece.

**O cadastro de animal pela clínica** (para um tutor de balcão) também fica de
fora: depende da área da equipe, que é a change seguinte.

## Capabilities

### New Capabilities

- `animais`: o Animal como registro do domínio — seus dados, o vínculo
  obrigatório com um tutor e quem pode lê-lo ou alterá-lo.

### Modified Capabilities

- `tutores`: a recusa por documento já cadastrado passa a usar uma mensagem
  genérica, com a distinção indo para o log em vez de para a resposta.

Não declarei em `tutores` que um tutor é dono de animais, embora tenha
chegado a parecer necessário: specs descrevem **comportamento**, e o
comportamento que importa — só o dono enxerga e altera — pertence inteiro a
`animais`. Declarar nos dois lugares seria duplicar, e duplicata em spec é
onde as duas versões começam a divergir.

A mudança em `tutores`, por outro lado, é real e não é sobre animais: ao
decidir que esta change não distingue "não existe" de "não é seu", ficou
visível que o cadastro **público** da change anterior distingue — e com isso
confirma, sem token nenhum, se um CPF é cliente da clínica. Numa clínica
veterinária isso é dado de saúde por inferência. Corrigir aqui, junto com a
decisão que o revelou, é mais honesto do que deixar a inconsistência de pé
esperando uma change futura.

## Impact

**Xano** (`workspace 169225`, API group `PetBits`)

- Tabela nova para o Animal, com o vínculo obrigatório ao tutor.
- Endpoints novos de listar, obter, criar e atualizar, todos resolvendo o
  tutor a partir da credencial — nunca de um identificador recebido.
- Provável função reutilizável para resolver "qual tutor é quem está
  pedindo", já que quatro endpoints precisam da mesma resposta.

**Aplicação Reflex**

- Operações de animal no cliente HTTP.
- State da tela de animais.
- A tela pós-login passa a listar os animais e a oferecer o cadastro.

**Restrição a respeitar**: o plano gratuito aceita 10 requisições a cada 20
segundos. Abrir a tela de animais não deve custar mais do que duas.

**Risco herdado**: a medição da change anterior mostrou que o Xano grava `0`,
e não nulo, em colunas de vínculo omitidas. Isso importa aqui porque o vínculo
do animal com o tutor é **obrigatório** — um animal com dono `0` não
pertenceria a ninguém e escaparia de qualquer filtro por dono.
