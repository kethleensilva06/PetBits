## Decisions

### D1. Índices só onde há filtro sem índice, em tabela que cresce

Levantados de todos os `where` de `apis/` e `functions/`. Tabelas de
configuração (colaborador, serviço, produto) têm dezenas de linhas e ficam sem
índice novo, seguindo a decisão já escrita em `tables/colaborador.xs`. Nenhum
índice único novo: os que importam (`user.email`,
`tutor.documento`) já existem, e um único sobre dado de teste antigo poderia
falhar na publicação.

### D2. Período, e não páginas, nos pedidos

Páginas de 50 quebrariam a busca da tela, o resumo e o CSV, que trabalham
sobre a lista inteira. Um período mantém tudo isso e limita o que cresce. O
padrão de 90 dias cobre o que a equipe acompanha no dia a dia; "todo o
período" continua a um clique.

O endpoint calcula `desde = agora - dias × 1 dia`. Com `dias` vazio ou 0,
`desde` é 0 e a mesma consulta traz tudo — sem duplicar as consultas por caso.
Os itens seguem o mesmo filtro, pela junção com o pedido.

### D3. Do painel, todo o período

O painel conta os pedidos esperando sem período. Ao abrir Pedidos a partir
dele, o período vai para "todo", para a lista bater com a contagem.

## Risks / Trade-offs

- Um pedido antigo ainda pendente não aparece nos 90 dias; aparece com "todo
  o período" e pelo painel.
