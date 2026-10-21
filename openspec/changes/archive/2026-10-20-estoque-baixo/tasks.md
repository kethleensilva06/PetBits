## 1. Backend

- [x] 1.1 `equipe_painel.xs`: contagens de esgotados e acabando; validar, publicar e conferir contra a lista de produtos

## 2. Tela

- [x] 2.1 `ESTOQUE_BAIXO`, `estoque_do_painel` e `estoque_baixo` em `petbits/painel.py`, com testes
- [x] 2.2 Painel: cartões de estoque; Produtos: filtro e selo colorido

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador, como equipe: os números batem com a lista filtrada

Medido: o painel no Xano deu 0 esgotados e 1 acabando, igual à lista de
produtos (Arranhador de papelão, 4); o único produto inativo com estoque 0
ficou de fora. Na tela, o clique abriu Produtos com Estoque baixo e só o
Arranhador, com o selo âmbar; Todos voltou a mostrar a lista inteira.
