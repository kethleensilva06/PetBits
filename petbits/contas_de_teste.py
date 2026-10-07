"""Contas de teste para o atalho `Alt+1` da tela de entrada.

As credenciais moram em `contas-de-teste.local.txt`, na raiz do projeto, que
o `.gitignore` exclui. É o mesmo arquivo e o mesmo formato que
`scripts/teste_duas_contas.py` já lê: uma linha que começa com maiúscula abre
um bloco e vira o rótulo dele; dentro do bloco, `email:` e `senha:`.

    EQUIPE — Otávio Lins
      email: otavio@exemplo.com
      senha: ...

    TUTOR — conta do cadastro público
      email: tutor@exemplo.com
      senha: ...

Nenhuma senha mora no código (AGENTS.md, Segurança). E este módulo só é
chamado pelo backend: a senha sai daqui para o formulário apenas quando a
conta é escolhida (design.md da change `atalho-contas-de-teste`, D2).
"""

import re
from pathlib import Path
from typing import TypedDict

ARQUIVO = Path(__file__).resolve().parent.parent / "contas-de-teste.local.txt"


class ContaDeTeste(TypedDict):
    rotulo: str
    email: str
    senha: str


def ler() -> list[ContaDeTeste]:
    """As contas do arquivo, na ordem em que aparecem.

    Arquivo ausente devolve lista vazia: a tela mostra como criá-lo, e a
    entrada continua funcionando. Bloco sem e-mail ou sem senha é ignorado —
    preencher só metade do formulário seria pior do que não listar.
    """
    if not ARQUIVO.exists():
        return []

    contas: list[ContaDeTeste] = []
    atual: dict[str, str] | None = None
    for linha in ARQUIVO.read_text(encoding="utf-8").splitlines():
        texto = linha.strip()
        if re.match(r"^[A-Z]", texto):
            atual = {"rotulo": texto}
            contas.append(atual)  # type: ignore[arg-type]
        elif atual is not None and ":" in texto:
            chave, _, valor = texto.partition(":")
            chave = chave.strip().replace("-", "").lower()
            if chave in ("email", "senha"):
                atual[chave] = valor.strip()
    return [c for c in contas if c.get("email") and c.get("senha")]
