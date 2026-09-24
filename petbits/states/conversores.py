"""Conversão entre os valores dos formulários HTML e o JSON do Xano.

O Xano devolve campos de data e hora como epoch em milissegundos, mas aceita
ISO 8601 na escrita. Os inputs HTML, por sua vez, trabalham com `AAAA-MM-DD`
e `AAAA-MM-DDTHH:MM`. Toda essa tradução acontece aqui, para que os States
lidem apenas com strings prontas.
"""

from datetime import date, datetime
from typing import Any, Optional

# --- do formulário para o Xano -------------------------------------------------


def para_data(valor: str) -> Optional[str]:
    """Input `type="date"` (AAAA-MM-DD) para o formato aceito pelo Xano."""
    return valor.strip() or None if valor else None


def para_data_hora(valor: str) -> Optional[str]:
    """Input `type="datetime-local"` para ISO 8601 **com fuso**.

    O input HTML não informa fuso nenhum: o que chega é a hora local de quem
    digitou. Se mandarmos assim, o Xano interpreta como UTC — uma consulta
    marcada para as 09:00 é gravada como 09:00 UTC e volta para a tela como
    06:00. Por isso o horário local é declarado explicitamente antes de enviar.
    """
    if not valor:
        return None
    try:
        momento = datetime.fromisoformat(valor)
    except ValueError:
        return None
    if momento.tzinfo is None:
        momento = momento.astimezone()
    return momento.isoformat()


# --- do Xano para a interface --------------------------------------------------


def de_data_hora(valor: Any) -> Optional[datetime]:
    """Campo `timestamp` do Xano para `datetime`.

    Aceita epoch em milissegundos (o padrão do Xano) e também ISO 8601, para
    o caso de o campo ter sido criado como texto.
    """
    if valor is None or valor == "":
        return None
    if isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        try:
            return datetime.fromtimestamp(valor / 1000)
        except (OverflowError, OSError, ValueError):
            return None
    try:
        return datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
    except ValueError:
        return None


def de_data(valor: Any) -> Optional[date]:
    """Campo `date` do Xano para `date`."""
    momento = de_data_hora(valor)
    return momento.date() if momento else None


def formatar_data_hora(valor: Any) -> str:
    """Campo de data e hora do Xano no formato exibido nas tabelas."""
    momento = de_data_hora(valor)
    return momento.strftime("%d/%m/%Y %H:%M") if momento else "-"


def formatar_data(valor: Any) -> str:
    """Campo de data do Xano no formato exibido nas tabelas."""
    dia = de_data(valor)
    return dia.strftime("%d/%m/%Y") if dia else "-"


def formatar_moeda(valor: Any) -> str:
    """Valor numérico do Xano com duas casas decimais."""
    try:
        return f"{float(valor or 0):.2f}"
    except (TypeError, ValueError):
        return "0.00"


# --- do Xano de volta para o formulário ---------------------------------------


def para_input_data(valor: Any) -> str:
    """Campo de data do Xano no formato do input `type="date"`."""
    dia = de_data(valor)
    return dia.isoformat() if dia else ""


def para_input_data_hora(valor: Any) -> str:
    """Campo de data e hora do Xano no formato do input `datetime-local`."""
    momento = de_data_hora(valor)
    return momento.strftime("%Y-%m-%dT%H:%M") if momento else ""


def para_numero(valor: Any) -> str:
    """Valor numérico do Xano como texto editável no formulário."""
    if valor is None or valor == "":
        return ""
    return str(valor)
