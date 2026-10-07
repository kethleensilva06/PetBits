"""Cliente da API de metadados do Xano.

É por aqui que tabela, função e endpoint sobem para o Xano, em vez de serem
colados à mão no painel: o arquivo `.xs` do repositório é a fonte, e o que
está no ar é consequência dele.

O token vem do `.env` (`XANO_META_TOKEN`), que é gitignored, e **nunca é
impresso** — nem em erro, nem em depuração.

Uso como biblioteca:

    from scripts.xano_meta import tabelas, endpoints, enviar_xs

Uso na linha de comando, para conferir que a credencial ainda vale:

    python scripts/xano_meta.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

PROJETO = Path(__file__).resolve().parent.parent
load_dotenv(PROJETO / ".env", override=True)

TOKEN = os.getenv("XANO_META_TOKEN", "").strip()
META = "https://x8ki-letl-twmt.n7.xano.io/api:meta"

# Conta nova (a antiga foi desvinculada em 30/09).
WORKSPACE = 169225
APIGROUP_PETBITS = 434335
APIGROUP_AUTH = 434333

_H = {"Authorization": f"Bearer {TOKEN}"}


class SemCredencial(RuntimeError):
    pass


def _exigir_token() -> None:
    if not TOKEN:
        raise SemCredencial(
            "XANO_META_TOKEN ausente no .env. Gere um token de metadados no "
            "painel do Xano (Settings > Metadata API) e grave no .env."
        )


def req(metodo: str, caminho: str, **kw):
    """Chamada na API de metadados. Devolve (status, corpo)."""
    _exigir_token()
    r = httpx.request(metodo, f"{META}{caminho}", headers=_H, timeout=60, **kw)
    try:
        corpo = r.json() if r.content else None
    except ValueError:
        corpo = r.text[:600]
    return r.status_code, corpo


def enviar_xs(metodo: str, caminho: str, fonte: str):
    """POST/PUT de XanoScript cru, como a API espera."""
    _exigir_token()
    r = httpx.request(
        metodo,
        f"{META}{caminho}",
        headers={**_H, "Content-Type": "text/x-xanoscript"},
        content=fonte.encode("utf-8"),
        timeout=60,
    )
    try:
        corpo = r.json() if r.content else None
    except ValueError:
        corpo = r.text[:600]
    return r.status_code, corpo


def xs(caminho_relativo: str) -> str:
    """Lê um arquivo XanoScript do repositório."""
    return (PROJETO / caminho_relativo).read_text(encoding="utf-8")


def _itens(corpo):
    if isinstance(corpo, dict):
        return corpo.get("items", [])
    return corpo or []


def tabelas() -> dict:
    """Mapa nome -> id das tabelas do workspace."""
    st, b = req("GET", f"/workspace/{WORKSPACE}/table")
    if st != 200:
        raise RuntimeError(f"não listou tabelas: {st} {b}")
    return {t["name"]: t["id"] for t in _itens(b)}


def endpoints(grupo: int = APIGROUP_PETBITS) -> dict:
    """Mapa **(verbo, nome) -> id** dos endpoints de um grupo.

    A chave é o par, e não o nome sozinho, porque um endpoint do Xano é
    identificado pelos dois: `GET equipe/servicos` e `POST equipe/servicos`
    são rotas diferentes com o mesmo nome. Chavear só pelo nome faz um
    publicar por cima do outro — o segundo push vira um PUT no id do
    primeiro, e a rota de leitura some sem erro nenhum, substituída pela de
    escrita. Aconteceu aqui, com quatro rotas de uma vez.
    """
    st, b = req("GET", f"/workspace/{WORKSPACE}/apigroup/{grupo}/api")
    if st != 200:
        raise RuntimeError(f"não listou endpoints: {st} {b}")
    return {(e.get("verb", "").upper(), e["name"]): e["id"] for e in _itens(b)}


def _verbo_e_nome(fonte: str) -> tuple[str, str]:
    """Lê o verbo e o nome da rota do próprio XanoScript.

    Passá-los à mão é a origem do erro acima: a fonte da verdade é o arquivo.
    """
    primeira = next(
        linha for linha in fonte.splitlines() if linha.strip().startswith("query ")
    )
    corpo = primeira.strip().removeprefix("query ").strip()
    nome, _, resto = corpo.partition(" ")
    nome = nome.strip().strip('"')
    verbo = "GET"
    for pedaco in resto.split():
        if pedaco.startswith("verb="):
            verbo = pedaco.removeprefix("verb=").strip("{} ").upper()
    return verbo, nome


def funcoes() -> dict:
    """Mapa nome -> id das funções do workspace."""
    st, b = req("GET", f"/workspace/{WORKSPACE}/function")
    if st != 200:
        raise RuntimeError(f"não listou funções: {st} {b}")
    return {f["name"]: f["id"] for f in _itens(b)}


def publicar_tabela(nome: str, caminho_xs: str) -> tuple[int, object]:
    """Cria a tabela se não existir; atualiza se existir."""
    existentes = tabelas()
    fonte = xs(caminho_xs)
    if nome in existentes:
        return enviar_xs("PUT", f"/workspace/{WORKSPACE}/table/{existentes[nome]}", fonte)
    return enviar_xs("POST", f"/workspace/{WORKSPACE}/table", fonte)


def publicar_funcao(nome: str, caminho_xs: str) -> tuple[int, object]:
    existentes = funcoes()
    fonte = xs(caminho_xs)
    if nome in existentes:
        return enviar_xs("PUT", f"/workspace/{WORKSPACE}/function/{existentes[nome]}", fonte)
    return enviar_xs("POST", f"/workspace/{WORKSPACE}/function", fonte)


def publicar_endpoint(
    caminho_xs: str, grupo: int = APIGROUP_PETBITS
) -> tuple[int, object]:
    """Publica um endpoint a partir do arquivo, criando ou atualizando.

    O verbo e o nome saem do próprio XanoScript — não são passados por fora,
    justamente para não poderem discordar dele. O content-type
    `text/x-xanoscript` é o que identifica a fonte; o caminho é o mesmo do
    CRUD normal, sem sufixo.
    """
    fonte = xs(caminho_xs)
    chave = _verbo_e_nome(fonte)
    existentes = endpoints(grupo)
    if chave in existentes:
        return enviar_xs(
            "PUT",
            f"/workspace/{WORKSPACE}/apigroup/{grupo}/api/{existentes[chave]}",
            fonte,
        )
    return enviar_xs("POST", f"/workspace/{WORKSPACE}/apigroup/{grupo}/api", fonte)


def apagar_endpoint(
    verbo: str, nome: str, grupo: int = APIGROUP_PETBITS
) -> tuple[int, object]:
    existentes = endpoints(grupo)
    chave = (verbo.upper(), nome)
    if chave not in existentes:
        return 404, "não existe"
    return req(
        "DELETE", f"/workspace/{WORKSPACE}/apigroup/{grupo}/api/{existentes[chave]}"
    )


def linhas(tabela_id: int, pagina: int = 1) -> list:
    """Conteúdo de uma tabela, para conferência e para semear dado de teste."""
    st, b = req("GET", f"/workspace/{WORKSPACE}/table/{tabela_id}/content", params={"page": pagina})
    if st != 200:
        raise RuntimeError(f"não leu o conteúdo de {tabela_id}: {st} {b}")
    return _itens(b)


def inserir_linha(tabela_id: int, dados: dict) -> tuple[int, object]:
    return req("POST", f"/workspace/{WORKSPACE}/table/{tabela_id}/content", json=dados)


def editar_linha(tabela_id: int, linha_id: int, dados: dict) -> tuple[int, object]:
    return req("PUT", f"/workspace/{WORKSPACE}/table/{tabela_id}/content/{linha_id}", json=dados)


def apagar_linha(tabela_id: int, linha_id: int) -> tuple[int, object]:
    return req("DELETE", f"/workspace/{WORKSPACE}/table/{tabela_id}/content/{linha_id}")


if __name__ == "__main__":
    try:
        _exigir_token()
    except SemCredencial as erro:
        print(erro)
        sys.exit(1)

    st, b = req("GET", f"/workspace/{WORKSPACE}")
    if st != 200:
        print(f"credencial recusada ou workspace inacessível: HTTP {st}")
        print(b)
        sys.exit(1)

    print(f"workspace {WORKSPACE} acessível: {b.get('name')!r}")
    print(f"tabelas: {sorted(tabelas())}")
    print(f"funções: {sorted(funcoes())}")
    for (verbo, nome) in sorted(endpoints()):
        print(f"  {verbo:7} {nome}")
