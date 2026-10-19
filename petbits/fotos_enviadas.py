"""Conferência da foto escolhida, antes de enviar (change `perfil-e-fotos`, D2).

É aviso rápido, não proteção: o Xano confere de novo o tipo e o tamanho do que
recebe e é quem recusa de verdade. Aqui só se poupa a espera de um envio que
não ia passar. Funções puras, para os testes chamarem sem Reflex.
"""

LIMITE_EM_BYTES = 5 * 1024 * 1024
EXTENSOES = ("jpg", "jpeg", "png", "webp")


class FotoRecusada(ValueError):
    """O motivo vai direto para a tela."""


def extensao_da_foto(nome_do_arquivo: str | None, tamanho: int) -> str:
    """A extensão em minúsculas, ou `FotoRecusada` com o motivo."""
    nome = (nome_do_arquivo or "").strip().lower()
    extensao = nome.rsplit(".", 1)[-1] if "." in nome else ""
    if extensao not in EXTENSOES:
        raise FotoRecusada("A foto precisa ser JPG, PNG ou WebP.")
    if tamanho <= 0:
        raise FotoRecusada("O arquivo escolhido está vazio.")
    if tamanho > LIMITE_EM_BYTES:
        raise FotoRecusada("A foto pode ter no máximo 5 MB.")
    return extensao


def url_da_foto(foto) -> str:
    """O endereço público da foto gravada no Xano, ou "" quando não há."""
    if isinstance(foto, dict):
        return foto.get("url") or ""
    return ""
