## Decisions

### D1. Acento no cliente HTTP, por tabela de palavras

`petbits/mensagens.py` troca palavras e expressões sem acento pelas certas
(`nao` → `não`, `invalido` → `inválido`, `nao esta` → `não está`…), com
limite de palavra e preservando a maiúscula inicial. Expressões antes de
palavras soltas: "esta" sozinha não muda — "Esta conta" é demonstrativo —, só
"nao esta" e "ja esta". `_detalhe` em `petbits/xano.py` passa a mensagem por
ela, e todas as telas recebem sem mudar nada.

Alternativa descartada: acentuar no Xano. Seriam dezenas de endpoints
republicados por texto, e o motivo de terem ficado sem acento não está
registrado — melhor não arriscar o que hoje funciona.

O teste roda a função sobre **todas** as mensagens do backend, lidas dos
`.xs`, e confere que não sobra palavra sem acento da lista.

### D2. Notificação com `rx.toast`

Os `aviso_*` do perfil deixam de ser texto na tela; o handler devolve
`rx.toast.success(...)`. Os erros continuam fixos, porque pedem ação.

### D3. Menu de celular com `rx.menu`

As pílulas ficam com `display` só a partir de `md`; abaixo disso, um
`rx.menu` com o nome da área atual abre as 9. No topo, o selo "Clínica", o
papel e o primeiro nome somem abaixo de `sm`.

### D4. Busca, filtro e quantidade no `LojaState`

`busca` e `categoria_filtro` alimentam a var `produtos_visiveis`, que a grade
passa a usar; a normalização de texto é a de `petbits/ilustracoes.py`.
`qtd_detalhe` começa em 1 a cada abertura e fica entre 1 e o estoque menos o
que já está no carrinho. O cabeçalho lê `LojaState.quantidade_no_carrinho`.

### D5. Máscara nos `set_*`

`petbits/mascaras.py` com `cpf` e `telefone`, funções puras: tiram o que não
é dígito, cortam no tamanho e formatam. Os `set_*` dos campos passam o valor
por elas. O CPF já é normalizado no backend; o telefone é gravado formatado.

### D6. `try/finally` na ponta a ponta

A parte da loja em `scripts/verificar_ponta_a_ponta.py` desativa o produto
num `finally`.

## Verificação

- `tests/test_mensagens.py` (todas as mensagens dos `.xs`), `tests/test_mascaras.py`,
  e o filtro da loja; a suíte toda.
- Navegador: uma recusa acentuada (senha errada); a notificação do perfil; o
  menu da clínica no celular e as abas na tela larga; busca, filtro,
  quantidade e o ícone do carrinho; máscaras no cadastro e no perfil.
- `openspec validate acabamentos-de-tela --strict`.
