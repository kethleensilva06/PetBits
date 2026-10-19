## Why

A `cliente-ilustrado` deu imagem à área do cliente, mas em ilustração plana,
e uma imagem só por categoria: a "Areia higiênica" aparecia com um cachorro
na banheira, porque é da categoria Higiene. Para a dona de um cachorro de
verdade, a casa e a loja ficam mais próximas com fotografia — e a foto de um
produto tem de mostrar aquele produto. Numa loja de verdade (como a Petlove),
clicar no produto abre a foto grande e o que se precisa saber para comprar.

## What Changes

- As 14 ilustrações SVG da área do cliente dão lugar a **fotografias**:
  cão, gato e outro animal (avatar por espécie); uma por categoria de
  produto mais a genérica; o banner da casa; e as três telas vazias.
- **Foto por produto:** cada produto do catálogo ganha a sua foto, escolhida
  pelo nome e pela descrição (16 hoje: os 15 de exemplo e a escova cadastrada
  pela equipe). A foto da categoria fica como reserva para produto novo.
- **Detalhe do produto:** clicar na foto ou no nome abre a foto grande, a
  categoria, a marca, a embalagem, a descrição, o preço, a disponibilidade,
  quantos já estão no carrinho e o botão de adicionar.
- As fotos vêm do Unsplash (licença livre), escolhidas uma a uma e baixadas
  com autorização para `assets/fotos/` em tamanho de tela (WebP), com autor e
  identificador de cada uma em `assets/fotos/CREDITOS.md`.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: as imagens da área do cliente passam a ser
  fotografias de licença livre com crédito; o produto tem foto própria.
- `produtos`: o cliente abre o detalhe de um produto da loja.

## Fora do escopo

- Foto enviada pelo tutor (perfil, animal): é a change `perfil-e-fotos`.
- A equipe enviar a foto de um produto novo: produto cadastrado depois usa a
  foto da categoria até ganhar a sua (uma change futura pode dar o upload à
  equipe, com o mesmo armazenamento da `perfil-e-fotos`).
- Gerar imagens por IA: não há ferramenta para isso neste projeto.
- Fotos na área da clínica ou nas portas de entrada.

## Impact

- Arquivos: `assets/fotos/*` e `assets/fotos/produtos/*` novos;
  `assets/ilustracoes/*` removidos.
- Código: `petbits/ilustracoes.py`, `petbits/states/loja_state.py`,
  `petbits/visual.py`, `petbits/pages/inicio.py`, `loja.py`, `agenda.py`;
  `tests/test_ilustracoes.py`.
- Backend e dependências: nenhum impacto.
