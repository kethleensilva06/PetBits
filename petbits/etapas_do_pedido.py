"""As etapas de um pedido em Meus pedidos (change `linha-do-tempo-do-pedido`).

O caminho é o de `equipe_pedido_situacao.xs`. Função pura, para testar sem o
Xano.
"""

# Até onde cada situação levou o pedido, sem contar o pagamento (D2):
# 0 recebido, 2 pronto ou enviado, 3 entregue.
_ALCANCE = {"pendente": 0, "pago": 0, "pronto_retirada": 2, "enviado": 2, "entregue": 3}


def etapas(situacao: str, entrega: str, forma_pagamento: str, pago_em) -> list[dict]:
    """Quatro etapas, cada uma com `rotulo`, `feita` e `atual`.

    O pedido cancelado devolve lista vazia: a tela mostra o aviso no lugar.
    """
    if situacao not in _ALCANCE:
        return []
    retirada = entrega == "retirada"
    pago = bool(pago_em)
    if pago:
        pagamento = "Pago"
    elif forma_pagamento == "na_loja":
        pagamento = "Pagar na retirada" if retirada else "Pagar na loja"
    else:
        pagamento = "Aguardando pagamento"
    rotulos = ["Pedido recebido", pagamento,
               "Pronto para retirada" if retirada else "Enviado",
               "Retirado" if retirada else "Entregue"]
    alcance = _ALCANCE[situacao]
    feitas = [i == 0 or (i == 1 and pago) or (i >= 2 and i <= alcance) for i in range(4)]
    # A atual é a seguinte à última feita (D3); entregue não tem atual.
    ultima = max(i for i, f in enumerate(feitas) if f)
    atual = ultima + 1 if ultima < 3 else None
    return [{"rotulo": r, "feita": f, "atual": i == atual}
            for i, (r, f) in enumerate(zip(rotulos, feitas))]


def finalizado(situacao: str) -> bool:
    """Entregue ou cancelado: não muda mais (change `pedidos-em-andamento`)."""
    return situacao in ("entregue", "cancelado")
