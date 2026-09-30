# AGENTS.md — PetBits

Regras de trabalho para agentes de IA neste projeto.

Este arquivo diz **como trabalhar**, não o que o projeto é. Para isso, leia
`docs/project-overview.md` e `docs/domain-model.md`.

## Documentação

Antes de qualquer alteração significativa, consultar os documentos de
contexto do projeto.

Quando uma decisão contrariar `docs/domain-model.md`, parar e tratar a
divergência — não implementar por cima dela.

## Desenvolvimento

Mudanças passam pelo OpenSpec: `Explore → Propose → Review → Apply →
Archive`.

Não implementar funcionalidade sem uma change correspondente em
`openspec/changes/`.

Cada change entrega uma **fatia vertical** — uma funcionalidade utilizável de
ponta a ponta. Não organizar changes por camada ("criar o banco", "criar o
frontend").

Não ampliar o escopo de uma change durante a implementação. Escopo novo é
change nova.

## Arquitetura

Respeitar as tecnologias definidas no projeto. Não introduzir tecnologias
alternativas sem uma mudança arquitetural explícita.

### Frontend

O frontend do projeto deve ser implementado exclusivamente com Reflex.

Utilizar os mecanismos próprios do Reflex para componentes, estado, eventos,
páginas e interação.

Não introduzir outra tecnologia de frontend para substituir ou complementar o
Reflex, salvo quando houver uma alteração arquitetural explicitamente
aprovada.

### Ambiente Python

`venv` + `pip`. Não utilizar `uv`, não criar `uv.lock`.

Ao adicionar uma dependência: verificar se é necessária, instalar no `.venv`,
testar, atualizar `requirements.txt` e versionar junto com a change
correspondente.

### Persistência

O banco de dados fica no Xano, acessado por HTTP. A aplicação Reflex não tem
banco local nem ORM.

## Segurança

Regras de autorização devem ser aplicadas no backend.

O frontend pode esconder o que não interessa, mas esconder não é proteger:
qualquer dado que chegue ao navegador é visível para quem souber olhar.

O papel do usuário é lido do banco a cada requisição, nunca do que o cliente
enviou.

Credenciais ficam em `.env`, que não é versionado. Nunca escrever credencial
em código, em documento ou em mensagem.

## Código

Reutilizar código existente quando apropriado. Evitar duplicação.

Não modificar funcionalidades não relacionadas à change atual sem
justificativa.

Escrever no idioma do projeto: identificadores, comentários e textos de
interface em português brasileiro.

## Testes

Mudanças funcionais devem possuir estratégia de verificação declarada na
change.

Verificar de fato antes de declarar concluído. Relatar o resultado como ele
é, inclusive quando falhar.
