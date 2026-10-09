## Context

A decisão da change `operacao-da-clinica` (D5) era que o destino viesse só do
papel, para a aba não virar oráculo de papel. O que torna a aba um oráculo é
ela influenciar **a verificação** ou **a resposta de recusa** — e nada disso
muda aqui.

## Goals / Non-Goals

**Goals:** a aba Cliente abrir a área de cliente para qualquer conta.

**Non-Goals:** mexer na verificação, no endpoint `/entrar` ou no que é
enviado ao servidor.

## Decisions

### D1 — A aba decide só depois da aceitação, e só no navegador

`AuthState.entrar` continua enviando e-mail e senha, e nada mais. A aba só é
lida **depois** do `/auth/me`, para escolher entre `/` e `/equipe`. Antes da
aceitação as duas abas são indistinguíveis: mesmo formulário, mesmo
manipulador, mesma requisição, mesma recusa. Depois da aceitação, a pessoa já
sabe o próprio papel — não há o que vazar.

### D2 — A regra mora em `rota_do_papel`, que nunca leva tutor à equipe

`rota_do_papel(papel, aba)` devolve `/equipe` **apenas** quando a conta é de
equipe **e** a aba é Colaborador. Qualquer outra combinação vai para `/`. A
área da equipe continua protegida pelo backend a cada requisição; a função só
evita mandar alguém para uma tela cheia de 403.

*Alternativa descartada:* tutor pela aba Colaborador receber aviso de "conta
não é da equipe". Seria a única diferença observável entre as abas na entrada
bem-sucedida — o oráculo que o D5 da change anterior existe para evitar.

## Risks / Trade-offs

- [Conta de equipe sem ficha de tutor na área de cliente] → Vê a lista vazia
  com o aviso de conta sem cadastro de tutor e o atalho "Abrir o painel". Não
  alcança dado de ninguém: a área de cliente só mostra o que o backend devolve
  para a ficha da própria conta.
