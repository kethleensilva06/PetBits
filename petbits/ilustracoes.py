"""Qual ilustração mostrar (change `cliente-ilustrado`, D2).

Funções puras, sem Reflex: os States as chamam ao montar cada item, junto com
o resto da formatação de tela, e os testes as chamam direto. As imagens são
arquivos de `assets/ilustracoes/`, servidos pelo próprio app — nenhuma
requisição ao Xano nem a serviço de fora.
"""

import unicodedata

PASTA = "/ilustracoes"

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


def imagem_da_especie(especie: str | None) -> str:
    palavra = _normalizar(especie)
    for imagem, nomes in _ESPECIES.items():
        if palavra in nomes:
            return f"{PASTA}/{imagem}.svg"
    return f"{PASTA}/outro.svg"


def imagem_da_categoria(categoria: str | None) -> str:
    """Recebe a chave crua (`racao`), não o rótulo de tela (`Ração`)."""
    chave = categoria if categoria in _CATEGORIAS else "outro"
    return f"{PASTA}/produto-{chave}.svg"
