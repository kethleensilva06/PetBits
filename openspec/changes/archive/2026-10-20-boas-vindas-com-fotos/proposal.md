## Why

A página inicial pública (`/boas-vindas`) é a primeira coisa que um visitante
vê, e hoje ela tem só a marca, uma frase e três cartões com ícones. As áreas
de dentro já usam fotos reais; a porta de entrada ficou para trás e não diz o
que a clínica oferece.

## What Changes

- Uma capa com a foto do banner (cão e gato), um título, uma frase sobre a
  clínica e os botões Entrar e Criar conta.
- Uma faixa "O que você encontra" com três fotos e textos curtos: Clínica
  (consultas e vacinas), Banho e tosa, e Petshop (ração, petiscos e
  brinquedos, com retirada ou entrega).
- Os três caminhos (cliente, equipe, primeira vez) continuam, abaixo.
- Só fotos que já estão em `assets/fotos/`, todas com crédito em `CREDITOS.md`.
  Nenhum download novo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: a página inicial pública apresenta a clínica com fotos.

## Fora do escopo

- Textos de preço, endereço ou horário da clínica (não estão no sistema).
- Mudar as entradas de clientes e da equipe.

## Impact

- Código: `petbits/pages/entrar.py` (`boas_vindas_page`); `tests/test_boas_vindas.py`.
