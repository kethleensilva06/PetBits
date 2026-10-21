"""O compromisso para a agenda do celular (change `agenda-guiada`, D4).

Um VCALENDAR com um VEVENT, conforme a RFC 5545: linhas com CRLF, horários
em UTC e texto escapado. Montado na tela, sem requisição.
"""

from datetime import datetime, timezone

LOCAL = "Clínica PetBits"


def _utc(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _texto(valor: str) -> str:
    """Escapa barra, ponto e vírgula, vírgula e quebra de linha (RFC 5545, 3.3.11)."""
    return (valor.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
            .replace("\r\n", "\\n").replace("\n", "\\n"))


def ics(*, uid: str, titulo: str, inicio_ms: int, fim_ms: int, descricao: str = "",
        agora_ms: int) -> str:
    linhas = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//PetBits//Agenda//PT-BR",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{_utc(agora_ms)}",
        f"DTSTART:{_utc(inicio_ms)}",
        f"DTEND:{_utc(fim_ms)}",
        f"SUMMARY:{_texto(titulo)}",
        f"LOCATION:{_texto(LOCAL)}",
    ]
    if descricao:
        linhas.append(f"DESCRIPTION:{_texto(descricao)}")
    linhas += ["END:VEVENT", "END:VCALENDAR"]
    return "\r\n".join(linhas) + "\r\n"
