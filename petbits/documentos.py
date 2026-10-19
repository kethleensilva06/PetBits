"""CPF válido pelos dígitos verificadores (change `cpf-valido`, D3).

A mesma conta da função `PetBits/cpf_valido` do Xano, aqui só para a tela
avisar na hora. A regra que vale é a do backend: sem esta conferência, o
cadastro é recusado do mesmo jeito.
"""


def so_digitos(texto: str | None) -> str:
    """Tira a pontuação que o backend também tira: ponto, traço, barra e espaço.

    Qualquer outro caractere fica — e faz o CPF ser inválido, como lá.
    """
    texto = texto or ""
    for c in ".-/ ":
        texto = texto.replace(c, "")
    return texto


def cpf_valido(texto: str | None) -> bool:
    cpf = so_digitos(texto)
    if len(cpf) != 11 or not cpf.isdigit() or len(set(cpf)) == 1:
        return False
    numeros = [int(c) for c in cpf]
    for tamanho in (9, 10):
        soma = sum(d * p for d, p in zip(numeros[:tamanho], range(tamanho + 1, 1, -1)))
        digito = (soma * 10) % 11
        if numeros[tamanho] != (0 if digito == 10 else digito):
            return False
    return True
