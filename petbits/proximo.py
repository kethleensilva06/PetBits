"""O próximo agendamento na casa do cliente (change `proximo-agendamento-na-casa`).

Funções puras, testadas sem o Xano.
"""

from datetime import datetime, timedelta

from petbits import agenda, rotulos

# Marcado, ou em andamento agora: ainda vem pela frente (D2).
_AINDA_VEM = ("marcado", "em_andamento")


def dia_legivel(inicio_ms: int, agora_ms: int) -> str:
    """"Hoje, 10:00", "Amanhã, 10:00" ou "Qua, 22 de outubro, 10:00" (D3)."""
    momento = datetime.fromtimestamp(inicio_ms / 1000, tz=agenda.FUSO)
    hoje = datetime.fromtimestamp(agora_ms / 1000, tz=agenda.FUSO).date()
    if momento.date() == hoje:
        dia = "Hoje"
    elif momento.date() == hoje + timedelta(days=1):
        dia = "Amanhã"
    else:
        dia = agenda.data_por_extenso(momento.date())
    return f"{dia}, {momento:%H:%M}"


def proximo_agendamento(registros, agora_ms: int) -> dict:
    """O de início mais cedo entre os que ainda não terminaram; {} se nenhum."""
    if not isinstance(registros, list):
        return {}
    futuros = sorted((a for a in registros if ainda_vem(a, agora_ms)),
                     key=lambda a: int(a.get("inicio") or 0))
    if not futuros:
        return {}
    a = futuros[0]
    profissional = " · ".join(filter(None, [
        a.get("profissional_nome") or "",
        rotulos.FUNCAO_LEGIVEL.get(a.get("profissional_funcao") or "", ""),
    ]))
    outros = len(futuros) - 1
    return {
        "titulo": f"{a.get('servico_nome') or 'Atendimento'} · {a.get('pet_nome') or '-'}",
        "quando": dia_legivel(int(a.get("inicio") or 0), agora_ms),
        "profissional": profissional,
        "em_andamento": a.get("situacao") == "em_andamento",
        "outros": "" if outros == 0 else (
            "mais 1 agendamento" if outros == 1 else f"mais {outros} agendamentos"),
    }


def ainda_vem(registro: dict, agora_ms: int) -> bool:
    """Marcado ou em andamento, e ainda não terminou (D2)."""
    return registro.get("situacao") in _AINDA_VEM and int(registro.get("fim") or 0) > agora_ms


def separar_agendamentos(registros: list[dict], agora_ms: int) -> tuple[list, list]:
    """Próximos (do mais perto ao mais longe) e anteriores (do mais recente ao
    mais antigo) (change `proximos-e-anteriores`)."""
    proximos = sorted((r for r in registros if ainda_vem(r, agora_ms)),
                      key=lambda r: int(r.get("inicio") or 0))
    anteriores = sorted((r for r in registros if not ainda_vem(r, agora_ms)),
                        key=lambda r: int(r.get("inicio") or 0), reverse=True)
    return proximos, anteriores
