"""A linha do tempo do histórico clínico (change `historico-clinico`).

Funções puras, sem Reflex: os States as chamam com o que o Xano devolveu, e
os testes as chamam direto.

Quem está retificado é calculado AQUI, pelos `retifica` da própria lista: o
atendimento original nunca é tocado no banco (D3). O Xano grava 0 em vínculo
omitido, então `retifica == 0` é "não é retificação".
"""

from datetime import date, datetime

from petbits import agenda
from petbits.rotulos import FUNCAO_LEGIVEL


def data_local(ms) -> str:
    """`DD/MM/AAAA` no fuso de São Paulo, ou "" sem data.

    O atendimento é um instante (pode ter sido registrado "agora"), então o
    dia é o de São Paulo, não o de UTC — às 22h daqui, em UTC já é amanhã.
    """
    if not ms:
        return ""
    try:
        return datetime.fromtimestamp(float(ms) / 1000, agenda.FUSO).strftime("%d/%m/%Y")
    except (TypeError, ValueError, OverflowError, OSError):
        return ""


def dia_em_ms(iso: str) -> int | None:
    """`AAAA-MM-DD` do campo de data → meia-noite de São Paulo, em ms."""
    if not iso:
        return None
    try:
        return agenda.inicio_do_dia_ms(date.fromisoformat(iso))
    except ValueError:
        return None


def _peso(valor) -> str:
    if valor in (None, "", 0, 0.0):
        return ""
    return f"{float(valor):.1f}".replace(".", ",").replace(",0", "") + " kg"


def linha_do_tempo(registros: list[dict]) -> list[dict]:
    """Cada atendimento pronto para a tela, o mais recente primeiro, com
    `retificado` e `retifica_data` calculados.

    No mesmo dia, o registrado por último vem antes: a data é só o dia, e sem
    o desempate a ordem entre dois atendimentos de um dia era a do banco.
    """
    registros = sorted(registros, key=lambda r: (r.get("data_atendimento") or 0, r.get("id") or 0),
                       reverse=True)
    por_id = {r.get("id"): r for r in registros}
    corrigidos = {r.get("retifica") for r in registros if r.get("retifica")}
    itens = []
    for r in registros:
        funcao = FUNCAO_LEGIVEL.get(r.get("colaborador_funcao") or "", "")
        quem = " · ".join(filter(None, [r.get("colaborador_nome") or "", funcao]))
        original = por_id.get(r.get("retifica")) if r.get("retifica") else None
        itens.append({
            "id": r.get("id"),
            "data": data_local(r.get("data_atendimento")),
            "quem": quem or "-",
            "motivo": r.get("motivo") or "",
            "diagnostico": r.get("diagnostico") or "",
            "tratamento": r.get("tratamento") or "",
            "peso": _peso(r.get("peso")),
            "retorno": data_local(r.get("retorno")),
            "retificado": r.get("id") in corrigidos,
            "e_retificacao": bool(r.get("retifica")),
            "retifica_data": data_local(original.get("data_atendimento")) if original else "",
            # Crus, para a equipe retificar com o formulário já preenchido.
            "_id_colaborador": r.get("id_colaborador") or 0,
            "_peso": "" if r.get("peso") in (None, 0, 0.0) else str(r.get("peso")),
        })
    return itens
