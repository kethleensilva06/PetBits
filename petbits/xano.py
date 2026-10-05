"""Cliente HTTP da API do Xano.

Único módulo do projeto que fala HTTP. Nenhuma outra parte deve montar URL,
cabeçalho ou tratar código de status.

São **dois** endereços, porque são dois API groups no Xano:

- `XANO_BASE_URL` — o grupo PetBits, com o domínio do projeto;
- `XANO_AUTH_BASE_URL` — o grupo Authentication, que veio pronto no workspace
  e tem o login e o perfil do usuário.

Ambos vêm do arquivo `.env` na raiz (veja `.env.example`).
"""

from __future__ import annotations

import os
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = httpx.Timeout(15.0)

GRUPO_PETBITS = "petbits"
GRUPO_AUTH = "auth"

# --- papéis -------------------------------------------------------------------
#
# O domínio fala em "tutor" e "equipe da clínica"; a tabela `user` do template
# grava "member" e "admin". Renomear o enum mexeria numa tabela da qual o login
# depende, sem ganho nenhum — então a tradução acontece aqui, num lugar só, e
# nenhuma outra parte do código compara com as strings cruas.

PAPEL_TUTOR = "member"
PAPEL_EQUIPE = "admin"


def eh_tutor(papel: str) -> bool:
    return papel == PAPEL_TUTOR


def eh_equipe(papel: str) -> bool:
    return papel == PAPEL_EQUIPE


def papel_legivel(papel: str) -> str:
    """O papel como a pessoa o vê na tela."""
    return "Equipe" if eh_equipe(papel) else "Tutor"


# --- erros --------------------------------------------------------------------


class XanoError(Exception):
    """Falha ao falar com o Xano, com mensagem pronta para mostrar na tela.

    As subclasses existem porque a interface precisa reagir de formas
    diferentes. A distinção que mais importa: **só credencial inválida encerra
    a sessão**. Uma falha de rede não pode expulsar ninguém do sistema — senão
    um Wi-Fi ruim vira logout — e um 403 significa que a pessoa está logada e
    apenas não pode aquilo.
    """

    def __init__(self, mensagem: str, *, status: int | None = None):
        super().__init__(mensagem)
        self.status = status


class SessaoExpirada(XanoError):
    """401 — a credencial não vale mais. Único caso que encerra a sessão."""


class FalhaDeComunicacao(XanoError):
    """Não deu para falar com o Xano. **Não** encerra a sessão."""


class SemPermissao(XanoError):
    """403 — autenticado, mas sem direito àquela operação."""


class CredenciaisInvalidas(XanoError):
    """E-mail ou senha incorretos na entrada."""


class DadosInvalidos(XanoError):
    """400 — o Xano recusou os dados enviados."""


class LimiteExcedido(XanoError):
    """429 — a cota de requisições do plano estourou."""


# --- requisição ---------------------------------------------------------------


def _base_url(grupo: str = GRUPO_PETBITS) -> str:
    variavel = "XANO_AUTH_BASE_URL" if grupo == GRUPO_AUTH else "XANO_BASE_URL"
    url = os.getenv(variavel, "").strip().rstrip("/")
    if not url:
        raise XanoError(
            f"{variavel} não configurada. Copie o endereço do API group no "
            "painel do Xano para o arquivo .env na raiz do projeto "
            "(veja .env.example)."
        )
    return url


def _headers(token: str = "") -> dict[str, str]:
    """Cabeçalhos da requisição. O token é o de quem está logado, quando há."""
    return {"Authorization": f"Bearer {token}"} if token else {}


def _detalhe(resposta: httpx.Response) -> str:
    """A mensagem de erro do corpo da resposta, quando existir."""
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

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as cliente:
            resposta = await cliente.request(
                metodo, url, headers=_headers(token), **kwargs
            )
    except httpx.HTTPError as erro:
        # Falha de transporte, não de autenticação. O tipo é distinto de
        # propósito: quem trata este erro não pode encerrar a sessão.
        raise FalhaDeComunicacao(
            f"Não foi possível falar com o Xano ({type(erro).__name__}). "
            "Verifique a conexão e o endereço configurado no .env."
        ) from erro

    if resposta.status_code == 401:
        raise SessaoExpirada(
            "Sua sessão expirou. Entre de novo para continuar.", status=401
        )
    if resposta.status_code == 403:
        raise SemPermissao(
            f"Você não tem permissão para esta operação. {_detalhe(resposta)}",
            status=403,
        )
    if resposta.status_code == 429:
        raise LimiteExcedido(
            "O Xano recusou a requisição por excesso de chamadas. Espere "
            "alguns segundos e tente de novo.",
            status=429,
        )
    if resposta.status_code == 404:
        # O Xano usa 404 para dois casos diferentes: o endpoint não existe, e
        # o registro pedido não existe. O primeiro é erro de configuração e
        # precisa aparecer; o segundo é resultado normal de uma busca.
        if "unable to locate request" in _detalhe(resposta).lower():
            raise XanoError(
                f"O endpoint {caminho} não existe no Xano. Confira se ele foi "
                "publicado no API group certo.",
                status=404,
            )
        return None
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


async def entrar(email: str, senha: str) -> dict:
    """Autentica e devolve `{authToken, ...}`.

    O Xano responde 403 tanto para senha errada quanto para e-mail
    inexistente, e em inglês. A tradução acontece aqui, e a mensagem é
    genérica de propósito: dizer "esse usuário não existe" permitiria
    descobrir quem tem conta no sistema.
    """
    try:
        return await _requisitar(
            "POST",
            "/auth/login",
            grupo=GRUPO_AUTH,
            json={"email": email, "password": senha},
        )
    except (SemPermissao, DadosInvalidos) as erro:
        raise CredenciaisInvalidas("E-mail ou senha incorretos.") from erro


async def usuario_atual(token: str) -> dict:
    """Perfil de quem está logado: `{id, name, email, role, ...}`."""
    return await _requisitar("GET", "/auth/me", grupo=GRUPO_AUTH, token=token)


async def cadastrar_tutor(
    nome: str,
    email: str,
    senha: str,
    documento: str,
    telefone: str = "",
    endereco: str = "",
) -> dict:
    """Cria a conta de acesso e a ficha de tutor numa requisição só.

    Devolve `{authToken, user_id, tutor_id}`. Não usa o `auth/signup` do
    template porque aquele cria apenas a conta — e a especificação exige que
    uma recusa não deixe conta órfã.
    """
    dados = {
        "nome": nome,
        "email": email,
        "password": senha,
        "documento": documento,
        "telefone": telefone or None,
        "endereco": endereco or None,
    }
    return await _requisitar("POST", "/tutor/cadastro", json=dados)


async def minha_ficha(token: str) -> Optional[dict]:
    """A ficha de tutor de quem está logado, ou None se a conta não tiver."""
    return await _requisitar("GET", "/me/tutor", token=token)


# --- animais ------------------------------------------------------------------
#
# O `token` e nomeado e **obrigatorio**, sem valor padrao. Esquece-lo falha na
# hora com TypeError, em vez de sair uma requisicao anonima que o backend
# recusa com 401 e faz a aplicacao deslogar sozinha -- o tipo de defeito que
# aparece como "as vezes ele me desconecta" e custa caro para achar.
#
# Nenhuma destas funcoes envia o dono: quem decide de quem e o animal e o
# backend, a partir da credencial.


async def listar_animais(*, token: str) -> list[dict]:
    """Os animais do tutor autenticado. Lista vazia quando nao ha nenhum."""
    dados = await _requisitar("GET", "/pet", token=token)
    return dados if isinstance(dados, list) else []


async def obter_animal(animal_id: int, *, token: str) -> Optional[dict]:
    """Um animal do tutor, ou None se nao for dele (ou nao existir)."""
    return await _requisitar("GET", f"/pet/{animal_id}", token=token)


class NaoEncontrado(XanoError):
    """O registro pedido nao existe, ou nao e de quem pediu.

    Os dois casos chegam aqui iguais de proposito: o backend responde o mesmo
    404 para "nao existe" e para "nao e seu", para nao permitir descobrir
    quantos registros existem.
    """


async def criar_animal(dados: dict, *, token: str) -> dict:
    """Cria um animal para o tutor autenticado."""
    criado = await _requisitar("POST", "/pet", token=token, json=dados)
    if criado is None:
        raise XanoError("O Xano nao confirmou a criacao do animal.")
    return criado


async def atualizar_animal(animal_id: int, dados: dict, *, token: str) -> dict:
    """Altera os campos informados de um animal do tutor.

    So o que estiver em `dados` e alterado: o backend monta a gravacao a partir
    do corpo recebido, entao um campo ausente aqui permanece como esta no
    banco. E o que impede uma edicao de apagar observacoes clinicas.

    Uma recusa por "nao encontrado" levanta `NaoEncontrado` em vez de devolver
    None. Sem isto, `_requisitar` traduz o 404 do backend para None -- que e o
    resultado legitimo de uma busca sem resultado -- e a tela mostraria como
    salva uma edicao que o backend recusou.
    """
    atualizado = await _requisitar(
        "PATCH", f"/pet/{animal_id}", token=token, json=dados
    )
    if atualizado is None:
        raise NaoEncontrado(
            "Este animal nao esta mais disponivel para edicao.", status=404
        )
    return atualizado
