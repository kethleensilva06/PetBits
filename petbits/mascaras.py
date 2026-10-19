"""CPF e telefone formatados enquanto se digita (change `acabamentos-de-tela`, D5).

Funções puras: tiram o que não é dígito, cortam no tamanho e formatam o que
já foi digitado — então funcionam a cada tecla, com o campo pela metade.
"""


def _digitos(texto: str | None, maximo: int) -> str:
    return "".join(c for c in (texto or "") if c.isdigit())[:maximo]


def cpf(texto: str | None) -> str:
    """`12345678909` → `123.456.789-09`; pela metade, `1234` → `123.4`."""
    d = _digitos(texto, 11)
    partes = [d[0:3], d[3:6], d[6:9]]
    corpo = ".".join(p for p in partes if p)
    return f"{corpo}-{d[9:]}" if len(d) > 9 else corpo


def telefone(texto: str | None) -> str:
    """`11988887777` → `(11) 98888-7777`; fixo `1133334444` → `(11) 3333-4444`."""
    d = _digitos(texto, 11)
    if not d:
        return ""
    if len(d) <= 2:
        return f"({d}"
    ddd, numero = d[:2], d[2:]
    corte = 5 if len(d) == 11 else 4
    if len(numero) <= corte:
        return f"({ddd}) {numero}"
    return f"({ddd}) {numero[:corte]}-{numero[corte:]}"
