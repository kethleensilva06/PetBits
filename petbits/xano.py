"""Cliente HTTP da API REST do Xano.

O banco de dados do PetBits fica hospedado no Xano, que expõe para cada tabela
os endpoints CRUD gerados automaticamente. Este módulo concentra toda a
comunicação com essa API: nenhuma outra parte do projeto deve falar HTTP.

Há dois API groups, com endereços diferentes:

- **PetBits** (`XANO_BASE_URL`) — as tabelas do domínio e o cadastro de tutor.
- **Authentication** (`XANO_AUTH_BASE_URL`) — login e perfil do usuário. Veio
  pronto no workspace e mora em outro `api:`, por isso a segunda variável.

Configuração (arquivo `.env` na raiz do projeto):

    XANO_BASE_URL=https://seu-workspace.xano.io/api:xxxxxxxx
    XANO_AUTH_BASE_URL=https://seu-workspace.xano.io/api:yyyyyyyy

Consulte `docs/xano-setup.md` para obter esses endereços.
"""

from __future__ import annotations

import asyncio
import os
import time
from collections import deque
from contextlib import asynccontextmanager
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = httpx.Timeout(15.0)

GRUPO_PETBITS = "petbits"
GRUPO_AUTH = "auth"

# O plano gratuito do Xano aceita 10 requisições a cada 20 segundos. O painel
# sozinho consulta sete tabelas, então sem controle o limite estoura na
# navegação normal. Pedimos até nove por janela (uma de folga) e, se mesmo
# assim o Xano responder 429, tentamos de novo depois de esperar.
#
# O limite é da instância, não do API group: os dois grupos dividem a mesma
# janela, por isso o controle é único e global a este módulo.
LIMITE_REQUISICOES = 9
JANELA_SEGUNDOS = 20.0
TENTATIVAS_LIMITE = 2
ESPERA_LIMITE = 6.0

_historico: deque[float] = deque()
_trava = asyncio.Lock()


@asynccontextmanager
async def _permissao_para_requisitar():
    """Segura a chamada até caber na janela de requisições do plano."""
    async with _trava:
        def _descartar_antigas():
            agora = time.monotonic()
            while _historico and agora - _historico[0] >= JANELA_SEGUNDOS:
                _historico.popleft()
            return agora

        agora = _descartar_antigas()
        if len(_historico) >= LIMITE_REQUISICOES:
            espera = JANELA_SEGUNDOS - (agora - _historico[0])
            if espera > 0:
                await asyncio.sleep(espera)
            _descartar_antigas()
        _historico.append(time.monotonic())
    yield

# Método HTTP do endpoint "Edit record" do Xano. Workspaces mais antigos geram
# esse endpoint como POST em vez de PATCH; nesse caso basta trocar esta
# constante — é o único lugar do projeto que decide isso.
METODO_ATUALIZAR = "PATCH"


class XanoError(Exception):
    """Falha ao falar com o Xano, com mensagem pronta para mostrar na tela.

    As subclasses existem para a interface poder reagir de formas diferentes.
    A regra que importa: **401 é a única coisa que desloga**. Um 403 significa
    que a pessoa está logada e apenas não pode aquilo, e uma falha de rede não
    pode expulsar ninguém do sistema — senão um Wi-Fi ruim vira logout.
    """

    def __init__(self, mensagem: str, *, status: int | None = None):
        super().__init__(mensagem)
        self.status = status


class SessaoExpirada(XanoError):
    """401 — o token não vale mais. Único caso que encerra a sessão."""


class SemPermissao(XanoError):
    """403 — autenticado, mas sem direito àquela operação."""


class CredenciaisInvalidas(XanoError):
    """E-mail ou senha incorretos no login."""


class EmailEmUso(XanoError):
    """Já existe conta com o e-mail informado."""


class DadosInvalidos(XanoError):
    """400 — o Xano recusou os dados enviados."""


class LimiteExcedido(XanoError):
    """429 mesmo depois das tentativas — a cota do plano estourou."""


def _base_url(grupo: str = GRUPO_PETBITS) -> str:
    variavel = "XANO_AUTH_BASE_URL" if grupo == GRUPO_AUTH else "XANO_BASE_URL"
    url = os.getenv(variavel, "").strip().rstrip("/")
    if not url:
        raise XanoError(
            f"{variavel} não configurada. Copie o base URL do API group no "
            "painel do Xano para o arquivo .env na raiz do projeto "
            "(veja docs/xano-setup.md)."
        )
    return url


def _headers(token: str = "") -> dict[str, str]:
    """Cabeçalhos da requisição. O token é o do usuário logado, quando há um."""
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


async def _requisitar(
    metodo: str,
    caminho: str,
    *,
    token: str = "",
    grupo: str = GRUPO_PETBITS,
    **kwargs,
) -> Any:
    """Executa uma requisição no Xano e devolve o JSON da resposta."""
    url = f"{_base_url(grupo)}{caminho}"

    for tentativa in range(TENTATIVAS_LIMITE + 1):
        async with _permissao_para_requisitar():
            try:
                async with httpx.AsyncClient(timeout=TIMEOUT) as cliente:
                    resposta = await cliente.request(
                        metodo, url, headers=_headers(token), **kwargs
                    )
            except httpx.HTTPError as erro:
                raise XanoError(
                    f"Não foi possível falar com o Xano ({type(erro).__name__}). "
                    "Verifique a conexão e o endereço configurado no .env."
                ) from erro

        if resposta.status_code != 429:
            break
        if tentativa == TENTATIVAS_LIMITE:
            raise LimiteExcedido(
                "O Xano recusou a requisição por excesso de chamadas. O plano "
                "gratuito aceita 10 requisições a cada 20 segundos. Espere "
                "alguns segundos e recarregue a página.",
                status=429,
            )
        await asyncio.sleep(ESPERA_LIMITE)

    if resposta.status_code == 404:
        # O Xano usa 404 para dois casos bem diferentes: o endpoint não existe
        # (e aí a mensagem é "Unable to locate request.") ou o registro pedido
        # não existe. O primeiro é erro de configuração e precisa aparecer na
        # tela; o segundo é resultado normal de uma busca por id.
        if "unable to locate request" in _detalhe(resposta).lower():
            raise XanoError(
                f"O endpoint {caminho} não existe no Xano. Confira se o CRUD "
                "da tabela foi criado no API group (veja docs/xanoscript.md).",
                status=404,
            )
        return None
    if resposta.status_code == 401:
        raise SessaoExpirada(
            "Sua sessão expirou. Entre de novo para continuar.", status=401
        )
    if resposta.status_code == 403:
        raise SemPermissao(
            f"Você não tem permissão para esta operação. {_detalhe(resposta)}",
            status=403,
        )
    if resposta.status_code == 400:
        raise DadosInvalidos(_detalhe(resposta), status=400)
    if resposta.status_code >= 400:
        raise XanoError(
            f"O Xano respondeu {resposta.status_code}: {_detalhe(resposta)}",
            status=resposta.status_code,
        )

    if not resposta.content:
        return None
    try:
        return resposta.json()
    except ValueError as erro:
        raise XanoError("O Xano devolveu uma resposta que não é JSON.") from erro


# --- autenticação -------------------------------------------------------------
#
# Os três vivem no API group Authentication, que veio pronto no workspace.


async def entrar(email: str, senha: str) -> dict:
    """Faz login e devolve `{authToken, user_id}`.

    O Xano responde 403 tanto para senha errada quanto para e-mail inexistente,
    e em inglês. A tradução acontece aqui para a tela receber um tipo próprio —
    e a mensagem é genérica de propósito: dizer "usuário não existe" permitiria
    descobrir quem tem conta.
    """
    try:
        return await _requisitar(
            "POST",
            "/auth/login",
            grupo=GRUPO_AUTH,
            json={"email": email, "password": senha},
        )
    except SemPermissao as erro:
        raise CredenciaisInvalidas("E-mail ou senha incorretos.") from erro


async def cadastrar_tutor(
    nome: str,
    email: str,
    senha: str,
    cpf: str,
    telefone: str = "",
    endereco: str = "",
) -> dict:
    """Cria o login e a ficha de tutor numa chamada só.

    Devolve `{authToken, user_id, cliente_id}`. O endpoint é do grupo PetBits
    (e não o `auth/signup` do template) porque grava também o cadastro de
    cliente, com o CPF, e checa os dois antes de criar qualquer coisa.
    """
    dados = {
        "nome": nome,
        "email": email,
        "password": senha,
        "cpf": cpf,
        "telefone": telefone or None,
        "endereco": endereco or None,
    }
    try:
        return await _requisitar("POST", "/cliente/signup", json=dados)
    except SemPermissao as erro:
        raise EmailEmUso("Já existe uma conta com esse e-mail.") from erro


async def usuario_atual(token: str) -> dict:
    """Perfil do usuário do token: `{id, name, email, account_id, role}`."""
    return await _requisitar("GET", "/auth/me", grupo=GRUPO_AUTH, token=token)


class TabelaXano:
    """Operações CRUD sobre uma tabela do Xano.

    Cada instância representa uma tabela e usa os endpoints REST que o Xano
    gera para ela. Os registros trafegam como dicionários JSON.

    O `token` é o do usuário logado. Ele é keyword-only e **obrigatório**: sem
    default, esquecer de passá-lo falha na hora com `TypeError`, em vez de sair
    uma requisição anônima que o Xano recusa com 401 e faz o app deslogar
    sozinho — o tipo de bug que aparece como "o sistema me desconecta às vezes"
    e custa caro para achar.
    """

    def __init__(self, nome: str):
        self.nome = nome

    async def listar(self, *, token: str) -> list[dict]:
        """Devolve todos os registros da tabela."""
        dados = await _requisitar("GET", f"/{self.nome}", token=token)
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

    async def obter(self, registro_id: int, *, token: str) -> Optional[dict]:
        """Devolve um registro pelo id, ou None se não existir."""
        return await _requisitar("GET", f"/{self.nome}/{registro_id}", token=token)

    async def criar(self, dados: dict, *, token: str) -> Optional[dict]:
        """Cria um registro e devolve o que o Xano gravou."""
        return await _requisitar("POST", f"/{self.nome}", token=token, json=dados)

    async def atualizar(
        self, registro_id: int, dados: dict, *, token: str
    ) -> Optional[dict]:
        """Atualiza os campos informados de um registro."""
        return await _requisitar(
            METODO_ATUALIZAR, f"/{self.nome}/{registro_id}", token=token, json=dados
        )

    async def remover(self, registro_id: int, *, token: str) -> None:
        """Remove um registro."""
        await _requisitar("DELETE", f"/{self.nome}/{registro_id}", token=token)

    async def listar_por(self, campo: str, valor: Any, *, token: str) -> list[dict]:
        """Devolve os registros em que `campo` é igual a `valor`.

        O CRUD gerado pelo Xano não aceita filtro na query string, então o
        filtro é aplicado depois de listar. Se o volume de dados crescer,
        crie um endpoint dedicado no Xano e troque só este método.
        """
        return [
            registro
            for registro in await self.listar(token=token)
            if registro.get(campo) == valor
        ]


async def minha_ficha(token: str) -> Optional[dict]:
    """A ficha de cliente do usuário logado. Admin não tem ficha e recebe None."""
    return await _requisitar("GET", "/me/cliente", token=token)
