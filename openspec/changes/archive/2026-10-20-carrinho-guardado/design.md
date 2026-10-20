## Decisions

### D1. O guardado é a fonte, o dicionário é derivado

`carrinho_salvo: str = rx.LocalStorage(...)` guarda o JSON; `carrinho` vira
uma var calculada a partir dele. Toda mudança passa por `_gravar(novo)`. Com
uma fonte só, o que está na tela e o que está guardado não divergem.

### D2. Ler com desconfiança

O valor vem do navegador e qualquer um o edita. `petbits/carrinho.py` lê o
JSON e só aceita id numérico com quantidade inteira entre 1 e 99; o resto é
descartado, e JSON quebrado vira carrinho vazio. Não é segurança — o
`POST pedidos` confere produto, preço e estoque no servidor —, é para a tela
não quebrar.

### D3. Conferido com o estoque ao abrir a loja

`carregar_loja` já reduzia o carrinho ao estoque que chegou. Agora isso vale
para o carrinho guardado, que pode ter dias.

### D4. Apagado ao sair

`limpar_dados`, chamado por `sair` e pelo fim de sessão, grava o carrinho
vazio. Quem entra depois no mesmo navegador não herda o carrinho de outra
pessoa.
