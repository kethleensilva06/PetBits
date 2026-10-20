## 1. Relatório

- [x] 1.1 `petbits/relatorio.py`: `resumo_de_pedidos` e `csv_de_pedidos`, com testes
- [x] 1.2 `EquipeState`: `resumo_pedidos` e `baixar_csv_pedidos`; o total cru em cada pedido
- [x] 1.3 Linha de resumo e botão Baixar CSV em Pedidos

## 2. Verificação

- [x] 2.1 Testes locais passam
- [x] 2.2 No navegador, como equipe: o resumo bate com os cartões; o CSV com o filtro

Medido na tela: com todos, "21 pedidos · R$ 499,30", a mesma soma dos cartões
não cancelados; com a busca "ana", "5 pedidos · R$ 92,30". O botão Baixar CSV
aparece; o arquivo não foi baixado no teste (salvaria na máquina da usuária),
e o conteúdo dele está coberto por `tests/test_relatorio.py`.
