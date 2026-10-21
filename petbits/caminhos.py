"""Caminhos das imagens do próprio site (change `site-no-github-pages`).

As fotos do app estão em `/fotos/...`, a partir da raiz do domínio. No Reflex
Cloud o site mora na raiz e isso basta; no GitHub Pages ele mora em
`/PetBits/`, e `/fotos/banner.webp` caía fora dele (404, medido).

`no_site` acrescenta o prefixo do site (`frontend_path`, fixado na compilação
de cada versão) só aos caminhos que começam com "/": a foto enviada por alguém
é um endereço completo do Xano e passa intacta. O servidor continua mandando
`/fotos/...` sem prefixo, porque é o mesmo para as duas versões do site.
"""

import reflex as rx
from reflex.config import get_config


def prefixo() -> str:
    """O prefixo da versão que está sendo compilada: "" ou "/PetBits"."""
    return get_config().frontend_path.rstrip("/")


def no_site(src):
    """O `src` de uma imagem, com o prefixo do site quando é caminho local."""
    base = prefixo()
    if not base:
        return src
    if isinstance(src, str):
        return base + src if src.startswith("/") else src
    texto = src.to(str)
    return rx.cond(texto.startswith("/"), base + texto, texto)
