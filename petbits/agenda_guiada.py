"""Os passos e o resumo da tela de agendar (change `agenda-guiada`, D1 e D2).

Funções puras: o `AgendaState` só passa os campos escolhidos.
"""

from petbits import agenda

ROTULOS_DOS_PASSOS = ("Serviço", "Animal", "Horário", "Confirmar")
FALTA = "a escolher"


def passos(servico_id: str, pet_id: str, horario_ms: int) -> list[dict]:
    """Cada passo feito ou não; a atual é a primeira não feita."""
    feitos = [bool(servico_id), bool(pet_id), bool(horario_ms), False]
    atual = feitos.index(False)
    return [{"numero": str(i + 1), "rotulo": rotulo, "feito": feito, "atual": i == atual}
            for i, (rotulo, feito) in enumerate(zip(ROTULOS_DOS_PASSOS, feitos))]


def linhas_do_resumo(servico: dict, animal: str, horario_ms: int,
                     dia_por_extenso: str) -> list[dict]:
    """Serviço, duração, preço, animal e quando; o que falta é "a escolher"."""
    if horario_ms:
        quando = f"{agenda.data_curta(horario_ms)} às {agenda.hora(horario_ms)}"
    elif dia_por_extenso:
        quando = f"{dia_por_extenso}, horário a escolher"
    else:
        quando = FALTA
    tem = bool(servico)
    return [
        {"rotulo": "Serviço", "valor": servico.get("nome") if tem else FALTA, "escolhido": tem},
        {"rotulo": "Duração", "valor": f"{servico['duracao']} min" if tem else FALTA,
         "escolhido": tem},
        {"rotulo": "Preço", "valor": servico.get("preco") if tem else FALTA, "escolhido": tem},
        {"rotulo": "Animal", "valor": animal or FALTA, "escolhido": bool(animal)},
        {"rotulo": "Quando", "valor": quando, "escolhido": bool(horario_ms)},
    ]
