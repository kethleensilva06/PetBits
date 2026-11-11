## Context

O token, o nome, o papel e a foto já são `rx.LocalStorage`. `sessao_validada`
não é persistida e força uma revalidação no Xano a cada nova sessão do
backend. O Xano emite o token com `expiration = 86400` (24 h) em `entrar.xs` e
`tutor_cadastro.xs`.

## Decisions

### D1. A validade fica no navegador, junto do token

`petbits_expira` (armazenamento local) guarda o instante, em segundos, em que a
sessão acaba: a entrada mais 12 horas. Conferir é uma comparação no servidor do
site, sem requisição, e por isso roda em **toda** abertura de página — antes do
atalho de `sessao_validada`, que só pula a ida ao Xano. A validade não se
estende ao navegar: 12 horas contadas da entrada.

Quem edita o armazenamento local para esticar a validade ganha, no máximo, as
24 horas do token do Xano, que continua decidindo de verdade.

### D2. "Não manter" é um cookie de sessão

Para a sessão acabar ao fechar o navegador e ainda assim valer em abas novas,
`sessionStorage` não serve (é por aba). Um cookie sem `max_age`
(`petbits_aberto`) é apagado pelo navegador ao fechar e é visto por todas as
abas. Ele não guarda segredo nenhum, só a marca "1". `petbits_lembrar`
(armazenamento local) diz qual dos dois modos a pessoa escolheu.

### D3. Uma função pura decide

`fim_da_sessao(token, expira_em, lembrar, aberto, agora)` devolve `""` (vale),
`"venceu"` ou `"fechou"`. Os testes falam com ela, sem montar o estado.

- Sem token: vale (não há o que encerrar).
- Validade ausente ou ilegível (sessões de antes desta change): `"fechou"`.
- Passou da validade: `"venceu"` — leva à entrada com o aviso.
- Modo "não manter" sem o cookie: `"fechou"` — sem aviso, como quem nunca
  entrou.

### D4. Onde é conferida

Em `_validar_sessao` (primeiro `on_load` de toda rota privada) e em
`redirecionar_se_logado` (página inicial, entrada e cadastro). Na página
inicial e no cadastro, a sessão vencida só é limpa; a pessoa fica onde está.

### D5. A caixa começa marcada

O pedido foi não precisar entrar de novo. Quem usa o computador da recepção
desmarca. `Sair` volta a caixa para marcada e apaga validade, modo e cookie.

## Risks / Trade-offs

- Uma aba aberta por mais de 12 horas continua funcionando até a próxima troca
  de página; o Xano recusa depois de 24 horas, e aí vale o aviso de sempre.
- Navegadores que restauram a sessão anterior ("continuar de onde parei")
  mantêm cookies de sessão: o modo "não manter" vira, ali, as 12 horas.
