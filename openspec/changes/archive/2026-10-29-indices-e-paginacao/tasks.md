## 1. Banco

- [x] 1.1 Índices novos em tutor, atendimento, agendamento e pedido
- [x] 1.2 `equipe/pedidos` com `dias`

## 2. Site

- [x] 2.1 `pedidos_da_clinica(situacao, dias)` e o filtro Período na tela
- [x] 2.2 Do painel, todo o período

## 3. Verificação

- [x] 3.1 XanoScript validado; testes locais passam
- [x] 3.2 Publicado no Xano; no navegador (localhost), Pedidos com 90 dias, 30 dias e todo o período

Publicado no Xano (4 tabelas e `equipe/pedidos`), com a autorização da
usuária. A guarda de equipe confere 29 endpoints, sem acusação.

Conferido no navegador (localhost), como equipe de teste: Pedidos abre com
"Últimos 90 dias" e mostra 21 pedidos. Direto no Xano, com a mesma conta:
todo o período e 90 dias, 21 pedidos e 26 itens; 7 dias e 1 dia, nenhum (os
pedidos de teste são de mais de uma semana atrás); em todos os casos, nenhum
item de pedido fora do período.

Os 236 testes passam.
