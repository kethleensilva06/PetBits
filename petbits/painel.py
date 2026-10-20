"""O painel da clínica: a resposta do `equipe/painel` pronta para a tela
(change `painel-do-dia`, D5).

Funções puras, para testar sem o Xano. O backend já tira os cancelados da
agenda e não manda contato de tutor; aqui só se formata.
"""

from petbits import agenda, rotulos

# Os pedidos que esperam a equipe, na ordem do caminho do pedido (D4):
# chave da resposta, situação do filtro de Pedidos, rótulo e ícone.
PEDIDOS_ESPERANDO = (
    ("pedidos_pendentes", "pendente", "Aguardando pagamento", "hourglass"),
    ("pedidos_pagos", "pago", "Pagos, a separar", "package"),
    ("pedidos_prontos", "pronto_retirada", "Prontos para retirada", "shopping-bag"),
)


def agenda_do_dia(registros) -> list[dict]:
    """Cada agendamento de hoje como linha do painel, em ordem de horário."""
    if not isinstance(registros, list):
        return []
    itens = []
    for a in sorted(registros, key=lambda r: r.get("inicio") or 0):
        itens.append({
            "id": a.get("id"),
            "horario": agenda.hora(a.get("inicio")),
            "animal": " · ".join(filter(None, [a.get("pet_nome") or "-",
                                               a.get("pet_especie") or ""])),
            "tutor": a.get("tutor_nome") or "-",
            "servico": a.get("servico_nome") or "-",
            "profissional": a.get("profissional_nome") or "-",
            "situacao": rotulos.SITUACOES_AGENDAMENTO.get(a.get("situacao") or "", "-"),
            "concluido": a.get("situacao") == "concluido",
        })
    return itens


def pedidos_esperando(dados: dict) -> dict[str, int]:
    """Quantos pedidos em cada situação que espera a equipe, mesmo com zero.

    Só os números: os cartões são fixos e montados na página a partir de
    `PEDIDOS_ESPERANDO` (o ícone do Reflex não aceita nome vindo do State).
    """
    return {situacao: int((dados or {}).get(chave) or 0)
            for chave, situacao, _rotulo, _icone in PEDIDOS_ESPERANDO}
