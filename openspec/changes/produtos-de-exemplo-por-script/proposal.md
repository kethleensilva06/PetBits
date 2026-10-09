## Why

A loja acabou de entrar no ar com o catálogo vazio, e testar a compra exige
produtos. Cadastrar 15 produtos à mão pela tela da equipe é lento, e o
cadastro exige uma conta de equipe logada — que só quem desenvolve tem.

## What Changes

- Script `scripts/criar_produtos_de_exemplo.py`, rodado por quem desenvolve,
  que entra com a **primeira conta de equipe com senha** do
  `contas-de-teste.local.txt` (a lista do `Alt+1`) e cadastra **15 produtos
  de exemplo** pelo mesmo `POST equipe/produtos` da tela.
- Os produtos cobrem as seis categorias da loja, com marca, unidade, preço e
  estoque plausíveis.
- Rodar de novo **não duplica**: produto com o mesmo nome já no catálogo é
  pulado.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `produtos`: um jeito de popular o catálogo com produtos de exemplo. (A
  capacidade nasce com a change `loja`, que é arquivada antes desta.)

## Fora do escopo

- Apagar produtos de exemplo.
- Fotos de produto.

## Impact

- Código: `scripts/criar_produtos_de_exemplo.py`; `README.md`.
- Xano: nenhum endpoint muda. Uma requisição de entrada, uma de conferência
  do papel, uma de listagem e uma por produto criado, com pausa pelo limite
  de 10 a cada 20 segundos.
