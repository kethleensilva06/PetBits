"""A busca das listas da clínica (change `busca-na-clinica`).

Filtra a lista que já está na tela: nenhuma requisição. Sem maiúscula nem
acento, e toda palavra digitada tem de aparecer em algum dos campos.
"""

from petbits.ilustracoes import normalizar


def _so_numeros(texto: str) -> str:
    return "".join(c for c in texto if c.isdigit())


_PONTUACAO_DE_NUMERO = set(".-()/ ")


def _numero_bate(palavra: str, numeros: str) -> bool:
    """A palavra é um número, com ou sem pontuação ("987.654", "(11)"), e os
    dígitos dela aparecem nos campos numéricos — gravados com ou sem máscara."""
    digitos = _so_numeros(palavra)
    so_numero = digitos and all(c.isdigit() or c in _PONTUACAO_DE_NUMERO for c in palavra)
    return bool(so_numero) and digitos in numeros


def filtrar(itens: list[dict], termo: str, campos: tuple[str, ...],
            numericos: tuple[str, ...] = ()) -> list[dict]:
    """Os itens em que cada palavra de `termo` aparece em `campos`.

    Os `numericos` (CPF, telefone) também são comparados só pelos números,
    para "12345" achar "123.45...".
    """
    palavras = normalizar(termo).split()
    if not palavras:
        return itens
    achados = []
    for item in itens:
        texto = " ".join(normalizar(str(item.get(c) or "")) for c in campos)
        numeros = " ".join(_so_numeros(str(item.get(c) or "")) for c in numericos)
        if all(p in texto or _numero_bate(p, numeros) for p in palavras):
            achados.append(item)
    return achados
