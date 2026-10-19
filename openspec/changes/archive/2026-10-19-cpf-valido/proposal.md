## Why

Hoje o cadastro de tutor só confere que o documento tem 11 dígitos. Assim,
`111.111.111-11` ou `123.456.789-00` criam conta e ficha de verdade, e a
ficha passa a ocupar aquele documento no índice único: a pessoa dona do CPF
digitado errado não consegue mais se cadastrar. Um CPF tem dois dígitos
verificadores justamente para pegar erro de digitação e número inventado.

## What Changes

- Função nova no Xano, `PetBits/cpf_valido`: confere os dois dígitos
  verificadores (módulo 11) e recusa os onze dígitos iguais.
- `POST tutor/cadastro` (cadastro público) e `POST equipe/tutores` (cadastro
  de balcão) chamam a função **antes de qualquer gravação** e recusam o CPF
  inválido com "CPF inválido. Confira os números.". Nenhuma conta nem ficha é
  criada.
- O Reflex faz a mesma conta antes de enviar, só para avisar na hora
  (`petbits/documentos.py`), nas duas telas. A regra que vale é a do backend.
- `scripts/criar_clientes_de_teste.py` passa a usar a função comum em vez da
  própria cópia.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `tutores`: o documento de identificação passa a ser um CPF válido pelos
  dígitos verificadores.

## Fora do escopo

- Confirmar que o CPF **pertence a uma pessoa real** ou ao nome digitado:
  isso exige consulta à Receita Federal ou a um serviço pago de terceiros, e
  o projeto exclui integração com sistemas externos. Os dígitos
  verificadores pegam erro de digitação e número inventado ao acaso, não um
  CPF válido de outra pessoa.
- Revalidar as fichas que já existem: elas continuam como estão.
- Aceitar documento estrangeiro ou CNPJ.

## Impact

- Xano: função nova; `tutor_cadastro.xs` e `equipe_tutor_create.xs`
  republicados por `scripts/publicar.py`.
- Reflex: `petbits/documentos.py` novo; `auth_state.py` e `equipe_state.py`.
- Testes: `tests/test_documentos.py`.
