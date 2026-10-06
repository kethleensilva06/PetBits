"""Conversão entre o `timestamp` do Xano e o que a tela mostra.

Vive num módulo próprio porque passou a ter dois usuários — os animais e os
colaboradores — e duas cópias de uma regra de data divergem em silêncio: a
primeira pessoa a corrigir uma delas não descobre que existe a outra.

**A distinção que estas funções codificam:** uma data de *calendário*
(nascimento, entrada na clínica) e um *instante* (o horário de um
atendimento) não se leem do mesmo jeito. O Xano recebe `2022-03-15` e guarda
a meia-noite **UTC** daquele dia. Lido em hora local (UTC−3), isso vira 14/03
às 21:00 — e a tela mostra o dia errado, sempre um a menos.

Por isso a leitura aqui é em UTC. Para um instante de verdade, o fuso importa
e a conversão tem de acontecer; quando essa necessidade chegar, ela ganha
funções próprias neste módulo, e não um `if` dentro destas.
"""

from datetime import datetime, timezone


def para_campo(valor) -> str:
    """O valor como o input `type="date"` espera: `AAAA-MM-DD`, ou vazio.

    O Xano guarda milissegundos e grava **0** quando o campo não foi
    informado — não nulo. Zero é 1970, não uma data: vira campo vazio.
    """
    if not valor:
        return ""
    try:
        return (
            datetime.fromtimestamp(float(valor) / 1000, tz=timezone.utc)
            .date()
            .isoformat()
        )
    except (TypeError, ValueError, OverflowError, OSError):
        return ""


def para_exibir(valor, vazio: str = "-") -> str:
    """A data como se lê em português: `DD/MM/AAAA`."""
    iso = para_campo(valor)
    if not iso:
        return vazio
    ano, mes, dia = iso.split("-")
    return f"{dia}/{mes}/{ano}"


def numero_para_campo(valor) -> str:
    """Número do Xano no campo de texto. Zero e nulo viram vazio."""
    if valor in (None, "", 0, 0.0):
        return ""
    return str(valor)
