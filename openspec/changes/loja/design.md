## Context

- Padrões já estabelecidos: posse pelo token (`tutor_do_token`) na escrita do
  cliente; `exige_equipe` em todo `equipe_*`, conferido pela guarda;
  alteração parcial pelo padrão `pick` (`equipe_servico_update.xs`);
  transação com `lock = true` contra corrida (`agendamento_create.xs`).
- Só operadores já executados pelo motor nesta conta: `>`, `==`, `!=`, `||`,
  `&&` (regra registrada em `equipe_servico_create.xs`).
- O modelo de domínio fixa: total derivado dos itens, preço unitário
  congelado, pedido sem itens não existe.

## Decisions

### D1 — Três tabelas

- `produto`: `nome`, `descricao?`, `categoria` (enum: `racao`, `petisco`,
  `brinquedo`, `higiene`, `acessorio`, `medicamento`), `marca?`, `unidade?`
  (texto livre: "un", "pacote 1 kg"), `preco` (decimal), `estoque` (int),
  `ativo` (bool).
- `pedido`: `id_tutor`, `situacao` (enum: `pendente`, `pago`,
  `pronto_retirada`, `enviado`, `entregue`, `cancelado`), `forma_pagamento`
  (`na_loja`, `online`), `entrega` (`retirada`, `endereco`),
  `endereco_entrega?`, `total` (decimal), `pago_em?`.
- `pedido_item`: `id_pedido`, `id_produto`, `produto_nome`, `quantidade`,
  `preco_unitario`, `valor_linha`.

`produto_nome` é congelado junto com o preço: o histórico do cliente diz o que
foi comprado mesmo que o produto mude de nome depois. As situações
`pronto_retirada`, `enviado` e `entregue` existem para a change
`pedidos-da-equipe`; esta só usa `pendente` e `pago`.

### D2 — O pedido inteiro numa transação, com trava por produto

`POST pedidos` recebe `itens` como `object[]` (`produto_id`, `quantidade`).
Dentro de um `db.transaction`, para cada item: lê o produto com `lock = true`,
confere ativo e estoque suficiente, baixa o estoque e soma a linha. Só então
grava o pedido e os itens. Qualquer recusa no meio desfaz tudo — o rollback do
`db.transaction` foi medido na change `acesso-do-tutor` (tarefa 2.7). A trava
serializa dois pedidos da mesma unidade: o segundo lê o estoque já baixado.

O `object[]` na entrada passa no parser oficial, mas **nunca rodou no motor
nesta conta**: é medido antes de o resto do endpoint depender dele.

### D3 — Pagamento online simulado

Com `forma_pagamento = online`, o pedido nasce `pago` com `pago_em = now`.
Nada é cobrado e nenhum dado de pagamento é pedido ou guardado; a tela diz
isso com todas as letras. Com `na_loja`, nasce `pendente`; quem registra o
pagamento é a equipe, na change seguinte.

### D4 — Endereço congelado

Com entrega no endereço, o `endereco` da ficha do cliente é copiado para o
pedido na hora da compra. Ficha sem endereço → recusa, com a orientação de
escolher retirada.

### D5 — Leitura do cliente em duas consultas

`GET pedidos` devolve os pedidos do cliente (join pedido → tutor → conta) e,
numa segunda consulta, os itens desses pedidos (join item → pedido → tutor →
conta). O Python agrupa. Duas consultas no Xano, uma requisição HTTP.

### D6 — Funcionário não usa a loja

`/loja` e `/pedidos` são área de cliente: o mesmo bloqueio da change
`porta-de-entrada` (D5) — conta de equipe vai para a gerência antes de
qualquer requisição.

## Risks / Trade-offs

- [`object[]` não funcionar no motor como o parser sugere] → Tarefa de medição
  antes do endpoint; a alternativa é `json itens` lido com filtros.
- [Pedido `pendente` prende estoque até a equipe agir] → É o comportamento
  esperado de reserva; cancelar e devolver estoque é da change seguinte.
- [Produto desativado com pedidos] → Os itens guardam nome e preço; o
  histórico não depende do produto continuar ativo.
