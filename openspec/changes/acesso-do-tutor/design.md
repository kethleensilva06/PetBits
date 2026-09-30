# Design

## Context

Ver `proposal.md` — Why. O que condiciona o desenho:

- O workspace do Xano (`169225`) já traz um template de autenticação:
  tabela `user` (com `email` único e `role` enum `admin|member`),
  `POST auth/login`, `GET auth/me` (que devolve o papel) e
  `POST auth/signup` (que fixa `role: "member"` no servidor). Login, troca de
  senha e os event logs dependem dessa tabela.
- O grupo `Authentication` mora em um `api:` **diferente** do grupo `PetBits`.
- A aplicação Reflex está em branco e ainda não fala HTTP com ninguém.
- O plano gratuito aceita 10 requisições a cada 20 segundos, por instância.
- Não há dado de produção: o workspace está vazio de conteúdo do domínio.

## Goals / Non-Goals

**Goals:**

- Estabelecer o padrão de sessão que todas as changes seguintes vão reusar.
- Deixar o modelo pronto para o tutor de balcão (sem conta), sem ter de
  desfazer nada depois.
- Manter o custo de entrar no sistema em duas requisições.

**Non-Goals:**

- Autorização por papel nas telas (é a change da área da equipe).
- Autorização por posse de dado (é a change dos animais).
- Recuperação de senha, embora o template já a ofereça: não é preciso agora e
  cada endpoint publicado é superfície a manter.

## Decisions

### D1 — Reaproveitar `auth/login` e `auth/me`; escrever o cadastro

O login do template já emite um token ligado à tabela `user`, e o `auth/me`
já devolve `role` no `output`. Escrever os nossos duplicaria o mecanismo de
token sem ganho.

O cadastro, porém, precisa ser novo: o `auth/signup` do template cria apenas
a conta, e a spec exige que a ficha de tutor nasça junto e que uma recusa não
deixe conta órfã. Um endpoint próprio no grupo `PetBits` faz as duas
gravações numa requisição.

*Alternativa descartada:* chamar `auth/signup` e depois criar o tutor pelo
cliente. São duas requisições e duas chances de falhar no meio — exatamente o
que a spec proíbe.

### D2 — O vínculo conta↔tutor mora no Tutor

A coluna que liga os dois fica na tabela do tutor, apontando para `user`.

*Alternativa descartada:* coluna em `user`. Aquela tabela é do template e dela
dependem login, troca de senha e event logs; um push errado ali derruba a
entrada de todo mundo. Mexer no que é nosso é mais barato de errar.

*Alternativa descartada:* tabela de ligação. É uma relação 0..1; uma tabela a
mais só acrescentaria uma junção em toda leitura.

### D3 — "No máximo um tutor por conta" é garantido pelo endpoint

A spec exige que uma conta não atenda a dois tutores, **e** que vários
tutores sem conta coexistam. Essas duas exigências brigam num índice único:
se o Xano gravar um valor padrão (por exemplo `0`) em vez de nulo quando não
há vínculo, o segundo tutor de balcão estoura o índice.

Decisão: a checagem é feita **no endpoint**, antes de gravar. Um índice único
entra depois apenas como reforço, e só se a verificação empírica mostrar que
a ausência de vínculo é gravada como nulo de verdade. Essa verificação é uma
tarefa, não um palpite.

*Por que não confiar só no índice:* porque a resposta depende de um
comportamento do Xano que ainda não foi medido nesta conta.

### D4 — Cadastro: conferir tudo antes de gravar qualquer coisa

Ordem: verificar o e-mail, verificar o documento, **então** criar a conta e
em seguida o tutor. Conferir o documento antes de criar a conta é o que
cumpre o cenário "recusa não deixa conta órfã" — invertido, a recusa por
documento duplicado aconteceria com a conta já criada.

Se o Xano oferecer `transaction` com rollback real, ela entra como reforço;
isso também é tarefa de verificação, não suposição.

### D5 — Sessão em armazenamento local do navegador

O token e o perfil ficam no armazenamento local, não numa variável de estado
comum. Motivo: o identificador que o Reflex usa para reconhecer o navegador
vive em `sessionStorage` e o estado do backend se perde quando o servidor
reinicia — uma variável comum não cumpre os três cenários de persistência da
spec.

Uma marca de "sessão já validada" fica **fora** do armazenamento local, de
propósito. Quando o backend não lembra mais deste navegador, ela volta ao
valor inicial e forçamos uma revalidação; nas demais navegações, economiza
uma requisição por página — o que importa dentro do orçamento de 10 por 20
segundos.

### D6 — A guarda mora dentro do carregamento, não só no `on_load`

O redirecionamento do Reflex é um evento de frontend e **não cancela** o que
já está na fila do backend. Um `on_load` com [validar sessão, carregar dados]
manda o redirecionamento ao navegador, mas o carregamento roda assim mesmo —
a requisição sai. A barreira que cumpre o cenário "nenhum dado da rota é
exibido **nem carregado**" é um retorno antecipado dentro de cada
carregamento.

Esta change tem uma única tela privada, então o custo agora é baixo; o valor
está em fixar o padrão antes de existirem nove.

### D7 — O token é parâmetro obrigatório de cada chamada

Cada operação no Xano recebe o token de quem está logado, como argumento
nomeado e **sem valor padrão**. Esquecer passa a ser um erro imediato, em vez
de sair uma requisição anônima que o backend recusa com 401 — o que a
aplicação interpretaria como sessão expirada e deslogaria a pessoa sozinha.

### D8 — Cliente HTTP assíncrono

Os event handlers do Reflex são assíncronos; um cliente síncrono bloquearia o
laço de eventos do servidor a cada requisição ao Xano. A biblioteca escolhida
precisa suportar `async`, e entra em `requirements.txt` junto com esta
change.

### D9 — Manter os valores `admin` e `member` do enum

O domínio fala em "equipe da clínica" e "tutor"; o template grava `admin` e
`member`. Renomear o enum na tabela `user` mexeria numa tabela da qual o
login depende, sem ganho funcional.

Decisão: manter os valores e registrar o mapeamento — `member` é tutor,
`admin` é equipe da clínica. A tradução acontece na fronteira da aplicação,
uma vez, não espalhada pelas telas.

## Risks / Trade-offs

**Conta órfã numa corrida** → D4 estreita muito a janela, mas entre conferir
e gravar cabe outra requisição. O índice único de `email` na tabela `user` é
o anteparo real: a segunda gravação falha. Fica registrado que a janela
existe.

**A verificação do nulo (D3) pode contrariar o índice único desejado** → por
isso a garantia primária é o endpoint, que funciona nos dois casos. O índice
é reforço opcional.

**Push para o Xano é irreversível por objeto** → validar todo `.xs` com o
parser oficial antes de empurrar, e empurrar em lotes pequenos conferindo
entre eles.

**Orçamento de requisições** → entrar custa 2 (login + perfil). O cadastro
custa 1 (endpoint único) + 1 (perfil). Ambos cabem com folga; a conta precisa
ser refeita quando a tela pós-login ganhar conteúdo.

**A extensão do Xano sobrescreve `AGENTS.md` ao entrar na conta** → já
mitigado: os arquivos gerados estão no `.gitignore` e o comando de
restauração está anotado no `CLAUDE.md`.

## Migration Plan

Não há dados a migrar: o workspace está vazio de conteúdo do domínio e a
aplicação está em branco.

**Subida:** validar os `.xs`, empurrar a tabela nova, empurrar os endpoints
novos, então subir a aplicação.

**Volta atrás:** `git revert` da change e novo push dos `.xs` anteriores. O
push do Xano é por objeto e não é transacional, então a volta é objeto a
objeto — mais uma razão para empurrar em lotes pequenos.

**Primeira conta de equipe:** fora do escopo desta change. Enquanto a área da
equipe não existir, o papel `admin` só é atribuído pelo painel do Xano.
