"""Conversão dos valores vindos dos formulários HTML para tipos do banco."""

from datetime import date, datetime
from typing import Optional


def para_data(valor: str) -> Optional[date]:
    """Converte o valor de um input `type="date"` (AAAA-MM-DD) em `date`."""
    return date.fromisoformat(valor) if valor else None


def para_data_hora(valor: str) -> Optional[datetime]:
    """Converte o valor de um input `type="datetime-local"` em `datetime`."""
    return datetime.fromisoformat(valor) if valor else None
