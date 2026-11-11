## 1. Rotas

- [x] 1.1 `/` e `/boas-vindas` na página inicial; a casa em `/animais`
- [x] 1.2 `ROTA_TUTOR`, menu, marca, Agenda e as guardas de sessão
- [x] 1.3 Testes ajustados

## 2. Verificação

- [x] 2.1 Testes locais passam
- [x] 2.2 No navegador (localhost): `/` sem sessão é a boas-vindas; a entrada de cliente leva a `/animais`; o menu e a marca também

Conferido no navegador (localhost): `/` sem sessão é a boas-vindas, sem
redirecionamento; a entrada de clientes, como Ana, levou a `/animais`, e o menu
"Meus animais" e a marca apontam para `/animais`; com sessão, abrir `/` levou a
`/animais`. Os 211 testes passam.
