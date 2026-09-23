"""Cliente HTTP da API REST do Xano.

O banco de dados do PetBits fica hospedado no Xano, que expõe para cada tabela
os endpoints CRUD gerados automaticamente. Este módulo concentra toda a
comunicação com essa API: nenhuma outra parte do projeto deve falar HTTP.

Configuração (arquivo `.env` na raiz do projeto ou variáveis de ambiente):

    XANO_BASE_URL=https://seu-workspace.xano.io/api:xxxxxxxx
    XANO_TOKEN=...     # opcional, apenas se o API group exigir autenticação

O `XANO_BASE_URL` é o "base URL" do API group, copiado do painel do Xano.
Consulte `docs/xano-setup.md` para criar as tabelas e obter esse endereço.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = httpx.Timeout(15.0)

# Método HTTP do endpoint "Edit record" do Xano. Workspaces mais antigos geram
# esse endpoint como POST em vez de PATCH; nesse caso basta trocar esta
# constante — é o único lugar do projeto que decide isso.
METODO_ATUALIZAR = "PATCH"


class XanoError(Exception):
    """Falha ao falar com o Xano, com mensagem pronta para mostrar na tela."""


def _base_url() -> str:
    url = os.getenv("XANO_BASE_URL", "").strip().rstrip("/")
    if not url:
        raise XanoError(
            "XANO_BASE_URL não configurada. Copie o base URL do API group no "
            "painel do Xano para o arquivo .env na raiz do projeto "
            "(veja docs/xano-setup.md)."
        )
    return url


def _headers() -> dict[str, str]:
    token = os.getenv("XANO_TOKEN", "").strip()
    return {"Authorization": f"Bearer {token}"} if token else {}


def _detalhe(resposta: httpx.Response) -> str:
    """Extrai a mensagem de erro do corpo da resposta, quando existir."""
    try:
        corpo = resposta.json()
    except ValueError:
        return resposta.text[:200] or "sem detalhes"
    if isinstance(corpo, dict):
        return str(corpo.get("message") or corpo.get("error") or corpo)[:200]
    return str(corpo)[:200]


async def _requisitar(metodo: str, caminho: str, **kwargs) -> Any:
    """Executa uma requisição no Xano e devolve o JSON da resposta."""
    url = f"{_base_url()}{caminho}"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as cliente:
            resposta = await cliente.request(
                metodo, url, headers=_headers(), **kwargs
            )
    except httpx.HTTPError as erro:
        raise XanoError(
            f"Não foi possível falar com o Xano ({type(erro).__name__}). "
            "Verifique a conexão e o valor de XANO_BASE_URL."
        ) from erro

    if resposta.status_code == 404:
        # O Xano usa 404 para dois casos bem diferentes: o endpoint não existe
        # (e aí a mensagem é "Unable to locate request.") ou o registro pedido
        # não existe. O primeiro é erro de configuração e precisa aparecer na
        # tela; o segundo é resultado normal de uma busca por id.
        if "unable to locate request" in _detalhe(resposta).lower():
            raise XanoError(
                f"O endpoint {caminho} não existe no Xano. Confira se o CRUD "
                "da tabela foi criado no API group (veja xano/README.md)."
            )
        return None
    if resposta.status_code in (401, 403):
        raise XanoError(
            "O Xano recusou a requisição (não autorizado). Verifique o "
            "XANO_TOKEN e as permissões do API group."
        )
    if resposta.status_code >= 400:
        raise XanoError(
            f"O Xano respondeu {resposta.status_code}: {_detalhe(resposta)}"
        )

    if not resposta.content:
        return None
    try:
        return resposta.json()
    except ValueError as erro:
        raise XanoError("O Xano devolveu uma resposta que não é JSON.") from erro


class TabelaXano:
    """Operações CRUD sobre uma tabela do Xano.

    Cada instância representa uma tabela e usa os endpoints REST que o Xano
    gera para ela. Os registros trafegam como dicionários JSON.
    """

    def __init__(self, nome: str):
        self.nome = nome

    async def listar(self) -> list[dict]:
        """Devolve todos os registros da tabela."""
        dados = await _requisitar("GET", f"/{self.nome}")
        if dados is None:
            return []
        if isinstance(dados, dict):
            # API groups com paginação ligada devolvem {"items": [...]}.
            dados = dados.get("items", [])
        if not isinstance(dados, list):
            raise XanoError(
                f"O endpoint /{self.nome} não devolveu uma lista de registros."
            )
        return [registro for registro in dados if isinstance(registro, dict)]

    async def obter(self, registro_id: int) -> Optional[dict]:
        """Devolve um registro pelo id, ou None se não existir."""
        return await _requisitar("GET", f"/{self.nome}/{registro_id}")

    async def criar(self, dados: dict) -> Optional[dict]:
        """Cria um registro e devolve o que o Xano gravou."""
        return await _requisitar("POST", f"/{self.nome}", json=dados)

    async def atualizar(self, registro_id: int, dados: dict) -> Optional[dict]:
        """Atualiza os campos informados de um registro."""
        return await _requisitar(
            METODO_ATUALIZAR, f"/{self.nome}/{registro_id}", json=dados
        )

    async def remover(self, registro_id: int) -> None:
        """Remove um registro."""
        await _requisitar("DELETE", f"/{self.nome}/{registro_id}")

    async def listar_por(self, campo: str, valor: Any) -> list[dict]:
        """Devolve os registros em que `campo` é igual a `valor`.

        O CRUD gerado pelo Xano não aceita filtro na query string, então o
        filtro é aplicado depois de listar. Se o volume de dados crescer,
        crie um endpoint dedicado no Xano e troque só este método.
        """
        return [
            registro
            for registro in await self.listar()
            if registro.get(campo) == valor
        ]
