"""O carrinho guardado no navegador (change `carrinho-guardado`, D2).

O valor vem do navegador, e qualquer um o edita: aqui só se garante que a
tela não quebre. Quem confere produto, preço e estoque é o `POST pedidos`.
"""

import json

MAXIMO_POR_PRODUTO = 99


def ler(texto: str) -> dict[str, int]:
    """O JSON guardado como {id do produto: quantidade}; o que não serve sai."""
    try:
        dados = json.loads(texto or "{}")
    except (ValueError, TypeError):
        return {}
    if not isinstance(dados, dict):
        return {}
    carrinho = {}
    for pid, qtd in dados.items():
        if (isinstance(pid, str) and pid.isdigit() and isinstance(qtd, int)
                and not isinstance(qtd, bool) and 1 <= qtd <= MAXIMO_POR_PRODUTO):
            carrinho[pid] = qtd
    return carrinho


def escrever(carrinho: dict[str, int]) -> str:
    return json.dumps({pid: qtd for pid, qtd in carrinho.items() if qtd > 0},
                      separators=(",", ":"))
