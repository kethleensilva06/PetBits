"""Qual imagem mostrar (change `cliente-ilustrado`, D2).

Funções puras, sem Reflex: os States as chamam ao montar cada item, junto com
o resto da formatação de tela, e os testes as chamam direto. As imagens são
fotos de licença livre em `assets/fotos/` (change `fotos-realistas`, D3),
servidas pelo próprio app — nenhuma requisição ao Xano nem a serviço de fora.
"""

import re
import unicodedata
from pathlib import Path

PASTA = "/fotos"

# A espécie é texto livre no cadastro do animal. Casa pela palavra, depois de
# tirar acento, maiúscula e espaço — "Cão", "cao" e " CACHORRO " são o mesmo.
_ESPECIES = {
    "cao": ("cao", "cachorro", "cachorra", "cadela", "cadelinha", "cachorrinho"),
    "gato": ("gato", "gata", "gatinho", "gatinha", "felino"),
}

_CATEGORIAS = ("racao", "petisco", "brinquedo", "higiene", "acessorio", "medicamento")


def _normalizar(texto: str | None) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in sem_acento if not unicodedata.combining(c)).strip().lower()


# Pública para a busca da loja (change `acabamentos-de-tela`, D4).
normalizar = _normalizar


def imagem_da_especie(especie: str | None) -> str:
    palavra = _normalizar(especie)
    for imagem, nomes in _ESPECIES.items():
        if palavra in nomes:
            return f"{PASTA}/{imagem}.webp"
    return f"{PASTA}/outro.webp"


# Fotos do próprio produto (change `fotos-realistas`): o arquivo leva o nome do
# produto em forma de chave — "Ração cães adultos 10 kg" vira
# `racao-caes-adultos-10-kg.webp`. Lido uma vez, na importação; produto sem foto
# própria (um que a equipe cadastrou depois) cai na foto da categoria.
_PASTA_PRODUTOS = Path(__file__).resolve().parent.parent / "assets" / "fotos" / "produtos"
_FOTOS_DE_PRODUTO = {f.stem for f in _PASTA_PRODUTOS.glob("*.webp")}


def chave_do_produto(nome: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", "-", _normalizar(nome)).strip("-")


def imagem_do_produto(nome: str | None, categoria: str | None, foto=None) -> str:
    """A foto enviada pela equipe vence (change `foto-do-produto`, D4); sem
    ela, a que acompanha o app pela chave do nome; sem essa, a da categoria.
    `foto` é o objeto de imagem do Xano, como vem no registro."""
    if isinstance(foto, dict) and foto.get("url"):
        return foto["url"]
    chave = chave_do_produto(nome)
    if chave in _FOTOS_DE_PRODUTO:
        return f"{PASTA}/produtos/{chave}.webp"
    return imagem_da_categoria(categoria)


def imagem_da_categoria(categoria: str | None) -> str:
    """Recebe a chave crua (`racao`), não o rótulo de tela (`Ração`)."""
    chave = categoria if categoria in _CATEGORIAS else "outro"
    return f"{PASTA}/produto-{chave}.webp"
