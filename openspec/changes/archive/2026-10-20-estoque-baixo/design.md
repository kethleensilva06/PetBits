## Decisions

### D1. Duas contagens, sem linha

`return = {type: "count"}` sobre `produto` ativo com `estoque == 0` e com
`estoque` entre 1 e 5. Pagam o próprio custo (regra do `equipe_painel.xs`):
são a pergunta "o que falta comprar", e não trazem nenhuma linha.

### D2. O limite é 5, num lugar só de cada lado

`ESTOQUE_BAIXO = 5` em `petbits/painel.py` e o mesmo 5 no `.xs`, com
comentário apontando um para o outro. O filtro de Produtos usa a constante
do Python.

### D3. Produto inativo não conta

Inativo já não está à venda; avisar que está acabando seria ruído.
