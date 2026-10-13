## Context

`POST pedidos` (change `loja`) tem a regra delicada da loja: para cada item,
ler o produto com trava, conferir ativo e estoque, baixar, congelar preço e
nome, somar; depois gravar pedido e itens, tudo numa transação. O balcão
precisa exatamente disso.

## Decisions

### D1 — A regra de estoque vira função

`PetBits/registrar_pedido` recebe `id_tutor`, `itens` (`object[]`),
`entrega`, `forma_pagamento`, `situacao`, `endereco` e `origem`, e faz a
transação inteira. `pago_em` nasce quando a situação é `pago` ou `entregue`.
`POST pedidos` passa a validar o que é do site (entrega, forma de pagamento,
endereço da ficha, dono pelo token) e chamar a função; `POST equipe/vendas`
valida o que é do balcão e chama a mesma função.

*Por que mexer num endpoint da change `loja`:* duas cópias da regra de
estoque divergiriam em silêncio — a primeira correção numa não chegaria na
outra. A função **não recebe preço nem total**: só produto e quantidade, como
o endpoint fazia.

### D2 — O balcão nasce entregue e pago

`entrega = retirada`, `forma_pagamento = na_loja`, `situacao = entregue`,
`origem = balcao`. O cliente pagou e levou; não há passo seguinte.

### D3 — O cliente vem do corpo, e a prova é de equipe

No site o dono é o token; no balcão quem pede é a equipe, então o
`tutor_id` vem da requisição. É seguro porque o endpoint é `equipe_*`, com
`exige_equipe` antes de tudo (e conferido pela guarda), e o cliente é lido do
banco antes de gravar: id inexistente é recusado.

### D4 — `origem` com padrão `site`

Coluna nova `enum origem?=site`. Os pedidos já existentes ficam `site`; o
`POST pedidos` passa `site` explicitamente.

## Registro da publicação (2026-10-09)

Pelo Xano CLI, procedimento da change `agendamento`, com os seis arquivos
nomeados um a um e `--dry-run` antes. O preview mostrou exatamente o
planejado: `UPDATE` e `ADD_FIELD` em `pedido` (a coluna `origem`), `CREATE`
da função `PetBits/registrar_pedido`, `CREATE` de `equipe/vendas POST` e
`UPDATE` de `pedidos GET`, `pedidos POST` e `equipe/pedidos GET` — nada mais.

Depois, a verificação de entrada sem token do `POST pedidos` republicado deu o
mesmo resultado da change `loja`: itens válidos → 401, item sem `produto_id`
→ 400. `equipe/vendas`, `pedidos` e `equipe/pedidos` sem token → 401. A
guarda confere 18 endpoints.

## Risks / Trade-offs

- [Republicar o `POST pedidos`] → A mudança é de forma (chamar a função), não
  de comportamento; `--dry-run` antes, e a mesma verificação de entrada sem
  token da change `loja` refeita depois.
