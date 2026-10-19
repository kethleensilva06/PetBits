"""Acentua as recusas que o backend devolve sem acento (change `acabamentos-de-tela`, D1).

Os endpoints do Xano escrevem "A senha atual nao confere."; a tela tem de
mostrar "A senha atual não confere.". A troca é por tabela, com limite de
palavra, e preserva a maiúscula inicial. Uma mensagem desconhecida passa como
veio: o pior caso é ela continuar sem acento, nunca ficar errada.

As EXPRESSÕES vêm antes das palavras soltas, e a ordem importa: "esta"
sozinha não muda — em "Esta conta" é demonstrativo —, só "nao esta" e
"ja esta" viram "não está" e "já está". O mesmo para "e" (conjunção em "a
nova senha e a confirmação") e "ha".
"""

import re

_EXPRESSOES = (
    ("nao esta", "não está"),
    ("ja esta", "já está"),
    ("nao e ", "não é "),
    ("quem e ", "quem é "),
    ("nao ha", "não há"),
    ("ha mais", "há mais"),
    ("esta incompleto", "está incompleto"),
    ("mais a venda", "mais à venda"),
)

_PALAVRAS = {
    "nao": "não",
    "invalido": "inválido",
    "invalida": "inválida",
    "invalidas": "inválidas",
    "invalidos": "inválidos",
    "numeros": "números",
    "digitos": "dígitos",
    "clinica": "clínica",
    "clinico": "clínico",
    "horario": "horário",
    "servico": "serviço",
    "preco": "preço",
    "funcao": "função",
    "situacao": "situação",
    "mudanca": "mudança",
    "gerencia": "gerência",
    "especie": "espécie",
    "duracao": "duração",
    "endereco": "endereço",
    "sessao": "sessão",
    "permissao": "permissão",
    "possivel": "possível",
    "unico": "único",
    "maximo": "máximo",
    "confirmacao": "confirmação",
    "valida": "válida",
    "valido": "válido",
    "ja": "já",
    "disponivel": "disponível",
    "area": "área",
}

_TRADUCOES = {
    "Passwords do not match!": "As senhas não conferem.",
    "No user found for that email.": "Nenhuma conta com esse e-mail.",
    "User not found with the provided ID.": "Conta não encontrada.",
    "email is required but was not suppiled. ": "Informe o e-mail.",
}


def _com_a_mesma_caixa(original: str, troca: str) -> str:
    return troca[0].upper() + troca[1:] if original[:1].isupper() else troca


def acentuar(texto: str) -> str:
    if not texto:
        return texto
    if texto in _TRADUCOES:
        return _TRADUCOES[texto]
    for sem, com in _EXPRESSOES:
        texto = re.sub(rf"\b{re.escape(sem)}", lambda m, com=com: _com_a_mesma_caixa(m.group(0), com),
                       texto, flags=re.IGNORECASE)
    padrao = re.compile(r"\b(" + "|".join(map(re.escape, _PALAVRAS)) + r")\b", re.IGNORECASE)
    return padrao.sub(lambda m: _com_a_mesma_caixa(m.group(0), _PALAVRAS[m.group(0).lower()]),
                      texto)
