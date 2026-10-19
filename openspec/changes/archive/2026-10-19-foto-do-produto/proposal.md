## Why

A loja acha a foto de um produto pela chave do nome: um arquivo em
`assets/fotos/produtos/<chave>.webp`, posto ali à mão por quem desenvolve.
Produto que a equipe cadastra depois, ou renomeia, perde a foto e cai na da
categoria — a "Escova removedora de pelos" só ganhou foto porque alguém a
baixou e salvou com o nome certo. A clínica mantém o catálogo sozinha, mas a
foto do que ela vende ainda depende de um commit.

## What Changes

- **Foto pela equipe:** no diálogo de edição de `/equipe/produtos`, a equipe
  envia a foto do produto, e troca quando quiser. O cartão do produto na
  tela da equipe passa a mostrar a mesma imagem que o cliente vê.
- **Loja usa a foto enviada:** o cartão e o detalhe do produto na loja
  mostram a foto enviada pela equipe quando ela existe; sem ela, continua a
  regra de hoje (foto pela chave do nome, depois a da categoria).
- **Backend (Xano):**
  - coluna opcional `foto` (imagem) em `produto`;
  - `POST equipe/produtos/{produto_id}/foto` — com a prova de equipe
    (`PetBits/exige_equipe`), recebe a imagem, confere extensão, conteúdo,
    tipo e tamanho e grava;
  - `GET loja/produtos` e `GET equipe/produtos` passam a incluir `foto` no
    `output`.
- `docs/domain-model.md` e `docs/project-overview.md` registram a foto do
  produto.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `produtos`: a equipe envia e troca a foto do produto; só a equipe.
- `identidade-visual`: a imagem do produto na loja passa a preferir a foto
  enviada pela equipe; e a regra "imagens sem custo de requisição" passa a
  dizer onde ficam as fotos enviadas por pessoas (armazenamento público do
  Xano), que a change `perfil-e-fotos` já tinha começado a usar para o tutor
  e o animal sem registrar na spec.

## Fora do escopo

- Apagar a foto de um produto (voltar à automática). Trocar é suportado;
  apagar fica para quando alguém pedir.
- Mais de uma foto por produto, galeria ou recorte na tela.
- Foto enviada no cadastro, antes de o produto existir: como no animal, a
  foto é gravada pelo id, então vem depois do primeiro "Salvar".
- Mudar a venda no balcão, que não mostra imagem.
- Tirar de `assets/fotos/produtos/` as fotos postas à mão: continuam como a
  segunda opção, para os produtos que a equipe não fotografou.

## Impact

- Xano: `tables/produto.xs`; endpoint novo `apis/pet_bits/equipe_produto_foto.xs`;
  `equipe_produto_list.xs` e `loja_produtos.xs` com `foto` no `output`;
  publicação por `scripts/publicar.py`.
- Reflex: `petbits/xano.py`, `petbits/ilustracoes.py` (`imagem_do_produto`
  aceita a foto enviada), `EquipeState` e `pages/equipe.py` (foto no
  diálogo e no cartão), `LojaState`.
- Docs: `docs/domain-model.md`, `docs/project-overview.md`.
- Dependências: nenhuma nova.
