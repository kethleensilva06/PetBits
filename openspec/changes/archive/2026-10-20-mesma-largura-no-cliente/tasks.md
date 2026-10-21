## 1. Largura

- [x] 1.1 `LARGURA_DO_CLIENTE` em `petbits/visual.py`, usada no container das cinco páginas
- [x] 1.2 `tests/test_largura.py`

## 2. Verificação

- [x] 2.1 Navegador: medir a largura do conteúdo nas cinco abas — **Medido em 20/10, tela de 1100 px:** antes, Loja 1053 px e as outras 880 px; depois, as cinco com 880 px. Na Loja, cada cartão de produto ficou com 286 px e o carrinho com 272 px, sem rolagem lateral
- [x] 2.2 `unittest` e `openspec validate mesma-largura-no-cliente --strict`
