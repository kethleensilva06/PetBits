## Decisions

### D1. Uma situação nova, não um campo

`faltou` entra no enum `situacao` de `agendamento`. Um agendamento tem uma
situação só, e falta é uma delas: não é cancelamento (que vem antes e libera
o horário) nem conclusão (que tem atendimento).

### D2. Só depois que o horário começou

`inicio <= agora`, pelo relógio do Xano. Marcar falta antes do horário é
erro de clique, e o horário ainda pode ser usado. Só `marcado`: concluído,
cancelado e falta não mudam.

### D3. Não desfaz

Como o histórico, a falta não se apaga nem volta a `marcado` por esta
change. Se foi engano, o caminho é marcar de novo.

### D4. Falta não vira atendimento

`equipe_atendimento_create.xs` exigia "nem cancelado nem concluído"; passa a
exigir `marcado` ou `em_andamento`, pela regra do projeto de escrever
condição por igualdade.

### D5. Ocupação

A ocupação ignora só `cancelado`, e continua assim: o horário com falta já
passou, então não há o que liberar.
