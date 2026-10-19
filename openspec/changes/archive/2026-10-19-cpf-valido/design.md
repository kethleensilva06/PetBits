## Context

`tutor/cadastro` e `equipe/tutores` normalizam o documento (tiram `.`, `-`,
`/` e espaço) e exigem 11 caracteres. As telas (`AuthState.cadastrar` e
`EquipeState` do balcão) repetem a contagem. `scripts/criar_clientes_de_teste.py`
já tem `cpf_ficticio` e `cpf_valido` próprios.

## Decisions

### D1. Uma função no Xano, chamada pelos dois endpoints

`PetBits/cpf_valido` recebe o documento já normalizado e devolve `true` ou
`false`. Os dois endpoints a chamam logo depois da normalização e antes de
`db.has` — antes de qualquer gravação, e também antes das consultas de
e-mail e documento em uso. Uma função só, como a `funcoes_da_categoria`:
duas cópias do cálculo divergem na primeira correção.

O cálculo: para o primeiro dígito, soma dos 9 primeiros com pesos 10..2;
para o segundo, dos 10 primeiros com pesos 11..2; o dígito é
`(soma * 10) % 11`, e 10 vira 0. Também exige só dígitos (a contagem de 11
sozinha aceitaria letras) e recusa os onze iguais.

Antes de escrever o laço, medir no Xano como ele se comporta com `for` e
`substr`/`split` numa string; se o laço não for confiável, desenrolar as
duas somas em expressões fixas (são só 9 e 10 termos).

### D2. A recusa por CPF inválido pode ser específica

A recusa genérica do cadastro existe para não revelar se um CPF é cliente
(`tutores`, "Documento de identificação único"). "CPF inválido" não revela
nada sobre a base: depende só do número digitado, e a mesma resposta sai
para qualquer pessoa. Então a mensagem diz o que corrigir, e ela vem antes
das conferências de uso, para que um CPF inválido nunca chegue a consultar
a tabela.

### D3. O Reflex avisa antes, com a mesma conta

`petbits/documentos.py` com `so_digitos` e `cpf_valido`, usado pelas duas
telas no lugar da contagem de 11 e pelo script de clientes de teste. É
conveniência: sem ela o backend recusa do mesmo jeito.

## Risks / Trade-offs

- [CPF válido de outra pessoa passa] → é o limite do método, declarado na
  proposta.
- [Ficha antiga com CPF inválido] → continua; só criação é conferida.

## Verificação

- `tests/test_documentos.py`: CPFs válidos conhecidos, dígito errado, onze
  iguais, letras, pontuação, vazio.
- `scripts/validar_xanoscript.mjs` nos três arquivos `.xs`; publicar com
  `--dry-run` antes.
- Contra o Xano de verdade, sem token e sem gravar nada que fique:
  `POST tutor/cadastro` com `123.456.789-00` e com `111.111.111-11` → 400 com
  a mensagem; conferir que nenhum `user` com aquele e-mail foi criado. Um CPF
  válido gerado por `cpf_ficticio` passa da conferência (criar com
  `scripts/criar_clientes_de_teste.py 1`).
- Balcão: no navegador, CPF inválido recusado; e chamada direta ao endpoint
  com token de equipe também recusada.
- `python -m unittest discover -s tests`, `scripts/verificar_equipe.py`,
  `openspec validate cpf-valido --strict`.
