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


def somar(atual: dict[str, int], itens: list[dict]) -> dict[str, int]:
    """Os itens de um pedido somados ao carrinho (change `comprar-de-novo`, D1).

    Item sem `id_produto` (0, de dado antigo) fica de fora.
    """
    novo = dict(atual)
    for item in itens:
        pid = str(item.get("id_produto") or "")
        qtd = int(item.get("quantidade") or 0)
        if pid.isdigit() and pid != "0" and qtd > 0:
            novo[pid] = min(novo.get(pid, 0) + qtd, MAXIMO_POR_PRODUTO)
    return novo


def ajustar_ao_estoque(carrinho: dict[str, int], estoque: dict[str, int]) -> tuple[dict, str]:
    """O carrinho cabendo no estoque, e o aviso do que mudou (D2).

    Produto fora da loja ou sem estoque sai; quantidade acima do estoque desce.
    """
    novo, saiu, reduzido = {}, 0, 0
    for pid, qtd in carrinho.items():
        disponivel = estoque.get(pid, 0)
        if disponivel <= 0:
            saiu += 1
            continue
        if qtd > disponivel:
            reduzido += 1
        novo[pid] = min(qtd, disponivel)
    partes = []
    if saiu:
        partes.append("1 item saiu do carrinho" if saiu == 1
                      else f"{saiu} itens saíram do carrinho")
    if reduzido:
        partes.append("1 item teve a quantidade reduzida" if reduzido == 1
                      else f"{reduzido} itens tiveram a quantidade reduzida")
    aviso = (" e ".join(partes) + ": sem estoque ou fora da loja.") if partes else ""
    return novo, aviso
