## Why

A usuária quer o site também no GitHub Pages do repositório. O Pages só serve
arquivos; o servidor do PetBits continua no Reflex Cloud
(`publicacao-no-reflex-cloud`). A parte visual pode morar no Pages e falar com
esse servidor.

## What Changes

- `scripts/publicar_no_github_pages.py`: compila a parte visual com o prefixo
  `/PetBits` (o Pages do repositório mora em
  https://kethleensilva06.github.io/PetBits/) e o endereço do servidor do Reflex
  Cloud, monta a pasta e, com `--publicar`, envia a branch `gh-pages`.
- O GitHub Pages passa a servir a branch `gh-pages` (servia a `main`, que só
  mostrava os arquivos do repositório).
- `petbits/caminhos.py`: `no_site(src)` põe o prefixo do site nas imagens do
  próprio app; sem ele, `/fotos/banner.webp` caía fora de `/PetBits/` (404).
  Foto enviada (endereço do Xano) passa intacta; no Reflex Cloud o prefixo é
  vazio e nada muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `publicacao`: o site também no GitHub Pages, ligado ao servidor do Reflex Cloud.

## Impact

- Código: `scripts/publicar_no_github_pages.py`, `petbits/caminhos.py` (novos);
  as imagens em `petbits/pages/` e `petbits/visual.py`;
  `tests/test_caminhos.py`, `tests/test_publicar_no_github_pages.py`; README.
- Repositório: branch `gh-pages` e a origem do GitHub Pages.
