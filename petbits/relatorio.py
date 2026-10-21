"""Resumo e exportação dos pedidos da clínica (change `resumo-dos-pedidos`).

Funções puras sobre a lista que já está na tela: nenhuma requisição. O CSV
não leva telefone, documento nem endereço do cliente.
"""

import csv
import io

from petbits.states.loja_state import reais

COLUNAS = ("Número", "Data", "Cliente", "Situação", "Entrega", "Pagamento", "Origem", "Itens",
           "Total")


def resumo_de_pedidos(pedidos: list[dict]) -> str:
    """"3 pedidos · R$ 60,00", sem os cancelados no total."""
    if not pedidos:
        return ""
    total = sum(float(p.get("_total") or 0) for p in pedidos if not p.get("_cancelado"))
    quantos = "1 pedido" if len(pedidos) == 1 else f"{len(pedidos)} pedidos"
    texto = f"{quantos} · {reais(total)}"
    if any(p.get("_cancelado") for p in pedidos):
        texto += " (cancelados não entram no total)"
    return texto


def csv_de_pedidos(pedidos: list[dict]) -> str:
    """Uma linha por pedido, separada por ponto e vírgula, como o Excel em
    português espera; o BOM no começo faz o Excel ler os acentos."""
    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=";", lineterminator="\r\n")
    escritor.writerow(COLUNAS)
    for p in pedidos:
        escritor.writerow([
            p.get("id"),
            p.get("quando") or "",
            p.get("_cliente_nome") or "",
            p.get("situacao") or "",
            p.get("entrega") or "",
            p.get("pagamento") or "",
            p.get("origem") or "",
            " | ".join(i.get("texto", "") for i in p.get("itens") or []),
            f"{float(p.get('_total') or 0):.2f}".replace(".", ","),
        ])
    return "﻿" + saida.getvalue()
