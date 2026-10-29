"""Leituras do Xano guardadas por um tempo (change `telas-guardadas`).

Uma camada só, em volta das funções de `xano.py` (D1): as leituras ganham
`@guardado(grupo, segundos)` e as gravações `@renova(*grupos)`. Nenhuma tela
muda.

A chave é o **token** de quem pediu (D2): o dado de uma pessoa só volta para
quem apresentar a mesma credencial, que já é o segredo da sessão. Tudo fica
na memória do servidor do site; nada vai para o navegador, porque o que se
guarda inclui CPF, endereço e observações clínicas, e o computador da
recepção é compartilhado.
"""

import copy
import functools
import time
from typing import Any

# token -> grupo -> chave -> (vale_ate, valor)
_GUARDADOS: dict[str, dict[str, dict[tuple, tuple[float, Any]]]] = {}

# Acima disto, cada nova entrada varre as vencidas (D6).
LIMITE_DE_ENTRADAS = 500

# Os scripts de verificação desligam: eles conferem, com duas contas, o que uma
# muda pela outra, e precisam ler sempre o backend.
ligado = True


def _token(args: tuple, kwargs: dict) -> str:
    """O token vem nomeado em quase todas as funções; `minha_ficha` o recebe
    na posição."""
    if "token" in kwargs:
        return kwargs["token"] or ""
    return args[0] if args and isinstance(args[0], str) else ""


def _entradas() -> int:
    return sum(len(chaves) for grupos in _GUARDADOS.values() for chaves in grupos.values())


def _varrer(agora: float) -> None:
    for token in list(_GUARDADOS):
        grupos = _GUARDADOS[token]
        for grupo in list(grupos):
            chaves = grupos[grupo]
            for chave in [c for c, (vale_ate, _) in chaves.items() if vale_ate <= agora]:
                del chaves[chave]
            if not chaves:
                del grupos[grupo]
        if not grupos:
            del _GUARDADOS[token]


def guardado(grupo: str, segundos: int):
    """Guarda o resultado da leitura por `segundos`, por token e argumentos.

    Sem token não guarda: não há de quem separar. Uma falha (exceção) não é
    guardada. Devolve sempre uma cópia, para a tela que mexer na lista não
    mexer no guardado.
    """
    def decorar(funcao):
        @functools.wraps(funcao)
        async def ler(*args, **kwargs):
            token = _token(args, kwargs)
            if not token or not ligado:
                return await funcao(*args, **kwargs)
            chave = (funcao.__name__, args, tuple(sorted(kwargs.items())))
            agora = time.monotonic()
            achado = _GUARDADOS.get(token, {}).get(grupo, {}).get(chave)
            if achado is not None and achado[0] > agora:
                return copy.deepcopy(achado[1])
            valor = await funcao(*args, **kwargs)
            if _entradas() >= LIMITE_DE_ENTRADAS:
                _varrer(agora)
            _GUARDADOS.setdefault(token, {}).setdefault(grupo, {})[chave] = (
                agora + segundos, copy.deepcopy(valor))
            return valor
        return ler
    return decorar


def renova(*grupos: str):
    """Depois da gravação, apaga esses grupos do token de quem gravou (D3).

    Apaga também quando a gravação falha: ela pode ter gravado em parte.
    """
    def decorar(funcao):
        @functools.wraps(funcao)
        async def gravar(*args, **kwargs):
            try:
                return await funcao(*args, **kwargs)
            finally:
                esquecer(_token(args, kwargs), *grupos)
        return gravar
    return decorar


def esquecer(token: str, *grupos: str) -> None:
    """Apaga os grupos do token; sem grupos, tudo dele (Sair e Atualizar)."""
    if not token or token not in _GUARDADOS:
        return
    if not grupos:
        del _GUARDADOS[token]
        return
    for grupo in grupos:
        _GUARDADOS[token].pop(grupo, None)
