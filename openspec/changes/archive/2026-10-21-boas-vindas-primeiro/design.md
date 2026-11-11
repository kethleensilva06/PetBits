## Decisions

### D1. A vitrine no endereço principal

Com `/` sendo a boas-vindas, o HTML que o visitante recebe primeiro já é a
vitrine, sem esperar o servidor. O `on_load` dela continua sendo só
`redirecionar_se_logado`: quem tem sessão vai para a sua área.

### D2. A casa em `/animais`

`ROTA_TUTOR` vira `/animais`, e com ele a entrada leva o cliente para lá. O
menu ("Meus animais"), a marca da área do cliente e o "Cadastrar" da Agenda
apontam para `/animais`. A guarda de sessão da casa, sem sessão, leva a `/`.

### D3. `/boas-vindas` continua

Quem guardou o endereço antigo, ou um link da documentação, não cai em "Página
não encontrada": a mesma página fica nos dois endereços.
