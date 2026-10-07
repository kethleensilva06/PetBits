"""Regras de tela da agenda: expediente, grade de horários e calendário.

Funções puras, sem Reflex e sem Xano, para poderem ser testadas sozinhas.

**Estas regras só SUGEREM.** Quem decide é o `POST agendamentos` no Xano, que
confere de novo expediente, grade, futuro e profissional livre (design.md da
change `agendamento`, D2). Se as duas versões divergirem, o pior caso é a tela
oferecer um horário que o backend recusa — nunca um agendamento inválido.

O fuso é fixo em UTC−3 (D3): o Brasil não tem horário de verão desde 2019. O
Xano usa `America/Sao_Paulo`; se o horário de verão voltar, a tela passa a
sugerir errado e o Xano recusa.
"""

import calendar
from datetime import date, datetime, time, timedelta, timezone

FUSO = timezone(timedelta(hours=-3))

PASSO_MINUTOS = 30
DIA_MS = 24 * 60 * 60 * 1000
PRAZO_CANCELAMENTO_MS = DIA_MS

# Expediente por dia da semana (0 = segunda ... 6 = domingo), em minutos
# desde a meia-noite. Decisão da clínica: seg–sex 8h–18h, sáb 8h–12h.
EXPEDIENTE: dict[int, tuple[int, int]] = {
    0: (8 * 60, 18 * 60),
    1: (8 * 60, 18 * 60),
    2: (8 * 60, 18 * 60),
    3: (8 * 60, 18 * 60),
    4: (8 * 60, 18 * 60),
    5: (8 * 60, 12 * 60),
}

CATEGORIAS = {"clinica": "Clínica", "banho_tosa": "Banho e tosa"}
SITUACOES = {
    "marcado": "Marcado",
    "em_andamento": "Em andamento",
    "concluido": "Concluído",
    "cancelado": "Cancelado",
}

DIAS_DA_SEMANA = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


def agora_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def hoje() -> date:
    return datetime.now(FUSO).date()


def inicio_do_dia_ms(dia: date) -> int:
    """Meia-noite daquele dia em São Paulo, em ms UTC — o `dia` dos endpoints."""
    return int(datetime.combine(dia, time(0, 0), tzinfo=FUSO).timestamp() * 1000)


def abre(dia: date) -> bool:
    return dia.weekday() in EXPEDIENTE


def horarios_livres(
    dia: date,
    duracao_minutos: int,
    profissionais: list[int],
    ocupados: list[dict],
    agora: int,
) -> list[int]:
    """Os inícios (ms UTC) em que há ao menos um profissional livre.

    Um início vale quando: está na grade de 30 minutos; o atendimento inteiro
    cabe no expediente; está no futuro; e algum profissional compatível não
    tem ocupação que cruze [início, fim). Dois intervalos se cruzam quando um
    começa antes de o outro terminar — encostados não se cruzam.
    """
    if not abre(dia) or duracao_minutos <= 0 or not profissionais:
        return []

    abertura, fechamento = EXPEDIENTE[dia.weekday()]
    meia_noite = inicio_do_dia_ms(dia)
    duracao_ms = duracao_minutos * 60_000

    ocupacoes: dict[int, list[tuple[int, int]]] = {}
    for item in ocupados:
        ocupacoes.setdefault(int(item["id_colaborador"]), []).append(
            (int(item["inicio"]), int(item["fim"]))
        )

    livres = []
    minuto = abertura
    while minuto + duracao_minutos <= fechamento:
        inicio = meia_noite + minuto * 60_000
        fim = inicio + duracao_ms
        if inicio > agora and any(
            not any(o_ini < fim and o_fim > inicio for o_ini, o_fim in ocupacoes.get(p, []))
            for p in profissionais
        ):
            livres.append(inicio)
        minuto += PASSO_MINUTOS
    return livres


def pode_cancelar(inicio_ms: int, agora: int) -> bool:
    """Até 24 h antes, como o backend confere (D6)."""
    return inicio_ms - agora >= PRAZO_CANCELAMENTO_MS


def semanas_do_mes(ano: int, mes: int) -> list[list[date | None]]:
    """O mês em semanas de segunda a domingo; `None` nas casas vazias."""
    return [
        [date(ano, mes, d) if d else None for d in semana]
        for semana in calendar.Calendar(firstweekday=0).monthdayscalendar(ano, mes)
    ]


def mes_vizinho(ano: int, mes: int, passo: int) -> tuple[int, int]:
    indice = ano * 12 + (mes - 1) + passo
    return indice // 12, indice % 12 + 1


# --- exibição -------------------------------------------------------------------


def _local(ms) -> datetime | None:
    try:
        return datetime.fromtimestamp(float(ms) / 1000, tz=FUSO)
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def hora(ms) -> str:
    momento = _local(ms)
    return momento.strftime("%H:%M") if momento else "-"


def data_curta(ms) -> str:
    momento = _local(ms)
    if not momento:
        return "-"
    return f"{DIAS_DA_SEMANA[momento.weekday()]}, {momento:%d/%m/%Y}"


def data_por_extenso(dia: date) -> str:
    return f"{DIAS_DA_SEMANA[dia.weekday()]}, {dia.day} de {MESES[dia.month - 1].lower()}"
