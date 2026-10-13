## Why

O petshop é o ramo do domínio que ainda não existe no sistema, e a clínica
pediu a loja: o cliente compra produtos pelo site, e a equipe cuida do
catálogo e dos pedidos. É a primeira de três changes da loja; esta entrega a
fatia que já funciona de ponta a ponta — a equipe põe produtos à venda e o
cliente compra.

## What Changes

- **Catálogo da equipe** (`/equipe/produtos`): cadastrar, alterar e
  ativar/desativar produtos, com categoria, marca, unidade de venda, preço e
  **estoque**.
- **Loja do cliente** (`/loja`): produtos ativos com estoque, carrinho e
  finalização do pedido escolhendo:
  - **entrega**: retirada na clínica ou entrega no endereço do cadastro;
  - **pagamento**: na loja (na retirada ou na entrega) ou **online
    simulado** — nenhum valor é cobrado; o pedido só é registrado como pago,
    com a forma de pagamento, na conta do cliente.
- **O pedido é calculado no servidor:** preço unitário congelado no momento da
  compra, valor de cada linha e total derivados — nada vem do navegador além
  de produto e quantidade.
- **Estoque baixa ao fazer o pedido**, dentro de uma transação com trava; a
  compra é recusada se pedir mais do que há.
- **Meus pedidos** (`/pedidos`): o cliente vê os pedidos dele, com itens,
  total, entrega, pagamento e situação.

## Capabilities

### New Capabilities

- `produtos`: o catálogo da loja, mantido pela equipe, com estoque.
- `pedidos`: a compra pelo cliente — itens, total, entrega, pagamento e o
  histórico do cliente.

### Modified Capabilities

Nenhuma.

## Fora do escopo (changes seguintes)

- **`pedidos-da-equipe`**: a equipe ver os pedidos, avançar a situação e
  cancelar devolvendo o estoque. Até lá, o pedido fica na situação em que
  nasceu.
- **`venda-no-balcao`**: o atendente registrar uma venda presencial na conta
  de um cliente.
- Pagamento real, frete, cupom, foto de produto.

## Impact

- Xano: tabelas novas `produto`, `pedido` e `pedido_item`; endpoints da
  equipe (`equipe/produtos` listar, criar, alterar) e do cliente
  (`loja/produtos`, `pedidos` listar e criar).
- Reflex: `/loja`, `/pedidos`, `/equipe/produtos`, menu da equipe e links na
  casa do cliente. Funcionário não usa a loja (mesma guarda da área de
  cliente).
- Orçamento de requisições: abrir a loja custa 1; finalizar custa 1; abrir
  "Meus pedidos" custa 1.
