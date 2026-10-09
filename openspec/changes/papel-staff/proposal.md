## Why

No painel do Xano, a coluna `role` da tabela `user` ganhou um terceiro valor,
`staff`, e contas de funcionário (como a do Otávio) foram marcadas com ele.
O sistema só reconhecia `admin` como equipe: para ele, `staff` era "papel
desconhecido". O funcionário entrava pela entrada da equipe e caía na área de
cliente como "Sem perfil", e o backend recusaria a gerência mesmo que ele
chegasse lá.

## What Changes

- `staff` passa a ser papel de equipe, com o **mesmo** acesso de `admin`.
- O backend (`PetBits/exige_equipe`) aceita `admin` **ou** `staff`, por
  igualdade com cada valor — nunca por negação de `member`.
- O Python (`eh_equipe`, `papel_conhecido`, `papel_legivel`) reconhece os dois.
- O repositório passa a registrar o enum que já está no Xano:
  `["admin", "staff", "member"]`. A tabela **não** é republicada — ela já está
  assim no Xano; o arquivo só deixa de mentir sobre ela.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `acesso-da-equipe`: quais valores de papel são de equipe.

## Fora do escopo

- Diferenciar permissões entre `admin` e `staff`. Se um dia gerente e
  funcionário precisarem alcançar coisas diferentes, é uma change própria.
- Mudar o papel de qualquer conta.

## Impact

- Xano: função `PetBits/exige_equipe`, republicada sozinha pelo Xano CLI.
  Todo endpoint `equipe_*` passa a aceitar `staff` por ela.
- Python: `petbits/xano.py`.
- Repositório: `tables/898256_user.xs` (só o registro do enum).
