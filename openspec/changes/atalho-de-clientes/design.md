## Context

O atalho da change `atalho-contas-de-teste` lê `contas-de-teste.local.txt`,
manda ao navegador só rótulo e e-mail, e na escolha relê o arquivo pelo
**índice** para preencher a senha (D2 daquela change).

## Decisions

### D1 — O grupo sai do rótulo, sem mudar o arquivo

`ler()` devolve também `grupo`: `clientes` quando o rótulo começa com `TUTOR`
ou `CLIENTE` (sem diferenciar maiúsculas), `equipe` nos demais. É a convenção
que o arquivo já usa e que `scripts/teste_duas_contas.py` já lê — nenhum
arquivo existente precisa ser reescrito.

### D2 — O índice é dentro do grupo aberto

A lista enviada ao navegador é a do grupo aberto, e o índice do clique é
relativo a ela. Na escolha, o backend relê o arquivo e **filtra pelo mesmo
grupo** antes de usar o índice; o grupo aberto fica no estado do servidor, e
não vem do clique. Assim um índice nunca aponta para uma conta de outro grupo.

## Risks / Trade-offs

- [Rótulo fora da convenção, como `Cliente — Ana` com minúsculas] → A
  comparação ignora maiúsculas; um rótulo que não comece com `TUTOR` nem
  `CLIENTE` cai na equipe, e aparece no `Alt+1`.
