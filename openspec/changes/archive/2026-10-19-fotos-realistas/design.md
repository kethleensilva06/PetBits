## Context

`petbits/ilustracoes.py` devolve caminhos de `/ilustracoes/*.svg`; as telas
usam `rx.image` com esses caminhos. `tests/test_ilustracoes.py` confere a
escolha e que cada arquivo existe.

## Decisions

### D1. Banco de licença livre, escolha feita na tela

Unsplash License e Pexels License permitem uso comercial sem pedir
autorização ao autor. Cada foto é escolhida vendo a página dela (não por
URL adivinhada), e a página é o que vai para os créditos. O download de cada
arquivo é feito só com autorização do usuário, com nome, origem e tamanho
informados antes.

Alternativa descartada: hotlink direto da CDN do banco. Faria a tela
depender de serviço de fora e mandaria a eles cada visita do cliente.

### D2. Tamanho de tela

Baixar na largura que a tela usa (cerca de 600 px; 1200 px para o banner),
pelo parâmetro de tamanho que o próprio banco oferece. Sem dependência nova
para redimensionar.

### D3. Mesmos nomes de função, outra pasta

`imagem_da_especie` e `imagem_da_categoria` mantêm a assinatura e passam a
devolver `/fotos/<nome>.<ext>`. Os States e as telas não mudam de forma; só
o `rx.image` ganha `object_fit="cover"`.

### D4. Foto por produto, pela chave do nome

A foto da categoria não descreve o produto ("Areia higiênica" com um cão na
banheira). Cada produto do catálogo ganha a sua em
`assets/fotos/produtos/<chave>.webp`, onde a chave é o nome sem acento, em
minúsculas, com hífens (`chave_do_produto`). `imagem_do_produto(nome,
categoria)` procura a foto própria e cai na da categoria. A lista de fotos é
lida uma vez, na importação.

Alternativa descartada por ora: guardar a foto no Xano, por produto. Daria à
equipe o poder de trocá-la, mas pede upload e armazenamento — o mesmo
caminho que a `perfil-e-fotos` abre; fica para uma change própria.

### D5. Detalhe do produto num diálogo, sem requisição

`LojaState.produto_aberto` recebe o item da própria lista da loja;
`quantidade_do_aberto` lê o carrinho. Diálogo e não página própria: a loja
já carregou tudo, e uma rota `/loja/<id>` teria de buscar o produto de novo.

## Risks / Trade-offs

- [Foto própria some se o produto for renomeado] → cai na da categoria; nada
  quebra.
- [Foto não é da marca vendida] → é do tipo de produto (uma tigela de ração,
  não o saco da marca); foto com marca de outro fabricante foi descartada na
  escolha. O nome e a marca continuam no texto.
- [Repositório público com fotos de terceiros] → as licenças permitem
  redistribuição; o crédito fica registrado.

## Verificação

- `tests/test_ilustracoes.py` atualizado: escolha e existência dos arquivos,
  e cada arquivo listado em `CREDITOS.md`.
- No navegador como tutora: casa (banner, avatares), loja, telas vazias; claro,
  escuro e celular; rede sem requisição a domínio externo além da fonte.
- `openspec validate fotos-realistas --strict`.
