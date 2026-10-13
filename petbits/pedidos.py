"""Caminhos de situação de um pedido (change `pedidos-da-equipe`, D2).

É a mesma tabela que `equipe_pedido_situacao.xs` confere no servidor. Aqui ela
só decide quais botões a tela da equipe oferece — quem recusa um caminho
inválido é o backend.
"""

ROTULOS_ACAO = {
    "pago": "Marcar como pago",
    "pronto_retirada": "Pronto para retirada",
    "enviado": "Marcar como enviado",
    "entregue": "Marcar como entregue",
    "cancelado": "Cancelar",
}


def proximas(situacao: str, entrega: str) -> list[str]:
    """As situações para as quais o pedido pode ir agora."""
    if situacao in ("pendente", "pago"):
        caminhos = []
        if situacao == "pendente":
            caminhos.append("pago")
        if entrega == "retirada":
            caminhos.append("pronto_retirada")
        if entrega == "endereco":
            caminhos.append("enviado")
        caminhos.append("cancelado")
        return caminhos
    if situacao == "pronto_retirada":
        return ["entregue", "cancelado"]
    if situacao == "enviado":
        return ["entregue"]
    return []
