## 1. Busca

- [x] 1.1 Texto de busca em cada pedido (número, cliente, produtos) e `pedidos_visiveis`
- [x] 1.2 Campo de busca em Pedidos, com "nada encontrado"
- [x] 1.3 Teste em `tests/test_busca.py`

## 2. Verificação

- [x] 2.1 Testes locais passam
- [x] 2.2 No navegador, como equipe: pelo número, pelo cliente e produto
- [x] 2.3 Achado na verificação: "14" trazia também os pedidos com 14 no telefone. Número de até 4 dígitos passou a procurar só o número do pedido (`filtrar_pedidos`); telefone, a partir de 5 dígitos
