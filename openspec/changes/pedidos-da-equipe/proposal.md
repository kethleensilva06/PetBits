## Why

Com a change `loja`, o cliente faz pedidos, mas eles ficam parados na
situação em que nasceram: ninguém na clínica os vê, registra o pagamento na
retirada, avisa que estão prontos ou cancela. É a segunda das três changes da
loja.

## What Changes

- **Pedidos da clínica** (`/equipe/pedidos`): a equipe vê todos os pedidos,
  do mais recente para o mais antigo, filtrando por situação, com cliente,
  telefone, itens, total, entrega, endereço e pagamento.
- **Avançar a situação**, só pelos caminhos válidos:
  - `pendente` → `pago`, `pronto_retirada` (retirada), `enviado` (entrega) ou
    `cancelado`;
  - `pago` → `pronto_retirada` (retirada), `enviado` (entrega) ou `cancelado`;
  - `pronto_retirada` → `entregue` ou `cancelado`;
  - `enviado` → `entregue`;
  - `entregue` e `cancelado` não mudam mais.
- **Pagamento na loja registrado pela equipe:** marcar como pago, ou entregar
  um pedido que ainda não tinha pagamento registrado, grava a data do
  pagamento — é o "paga na retirada".
- **Cancelar devolve o estoque** de cada item, numa transação.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pedidos`: a equipe acompanha e avança os pedidos; cancelar devolve
  estoque. (A capacidade nasce com a change `loja`, arquivada antes desta.)

## Fora do escopo

- Estorno de pagamento online (o pagamento é simulado).
- O cliente cancelar o próprio pedido.
- Venda presencial: change `venda-no-balcao`.

## Impact

- Xano: `GET equipe/pedidos` e `POST equipe/pedidos/{id}/situacao`.
- Reflex: `/equipe/pedidos` e o item no menu da equipe.
