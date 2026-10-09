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

ROTA_EQUIPE = "/equipe"
ROTA_TUTOR = "/"


def eh_tutor(papel: str) -> bool:
    return papel == PAPEL_TUTOR


def eh_equipe(papel: str) -> bool:
    return papel == PAPEL_EQUIPE


def papel_conhecido(papel: str) -> bool:
    """A coluna `role` é opcional no Xano, então vazio é um estado real.

    Uma conta de equipe nasce à mão no painel, e esquecer a coluna é o erro de
    operação mais provável do projeto — é assim que o primeiro admin da
    clínica vai ser criado.
    """
    return papel in (PAPEL_TUTOR, PAPEL_EQUIPE)


def papel_legivel(papel: str) -> str:
    """O papel como a pessoa o vê na tela.

    A versão anterior devolvia "Tutor" para tudo que não fosse `"admin"`, e
    por isso uma conta sem papel caía na área do tutor, não achava ficha
    nenhuma e lia "Nenhum animal cadastrado ainda" — o sintoma absurdo que
    esta change existe para matar. Papel desconhecido agora se chama pelo
    nome.
    """
    if eh_equipe(papel):
        return "Equipe"
    if eh_tutor(papel):
        return "Tutor"
    return "Sem perfil"


def rota_do_papel(papel: str) -> str:
    """Para onde a pessoa vai **depois** de a credencial ser aceita.

    Só o papel decide, vindo do `/auth/me` (change `porta-de-entrada`, D1 e
    D5): conta de equipe vai sempre para a gerência, por qualquer entrada, e o
    resto para a área de cliente. A página de entrada usada nunca é enviada
    ao servidor nem pesa aqui. Papel desconhecido vai para a área do tutor,
    onde um aviso explícito diz o que aconteceu — e, como a conta não tem
    ficha, ela não alcança dado de ninguém.
    """
    return ROTA_EQUIPE if eh_equipe(papel) else ROTA_TUTOR


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


def _contar_para_medicao(metodo: str, caminho: str) -> None:
    """Registra cada chamada ao Xano num arquivo, quando `PETBITS_MEDIR` aponta
    para um.

    Existe porque o orçamento do plano é de 10 requisições a cada 20 segundos
    **por instância**, e o custo de uma tela é uma afirmação que o design faz
    em números — então precisa ser medível, e não só argumentada. O painel do
    navegador não serve para isto: ele vê o WebSocket do Reflex, e as chamadas
    ao Xano saem do backend Python, onde ele não enxerga.

    Desligado por padrão: sem a variável de ambiente, não faz nada.
    """
    destino = os.getenv("PETBITS_MEDIR", "").strip()
    if not destino:
        return
    try:
        with open(destino, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{metodo} {caminho}\n")
    except OSError:
        # Medição nunca pode derrubar a aplicação.
        pass


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

    _contar_para_medicao(metodo, caminho)

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
    """Autentica e devolve `{authToken, user_id}`.

    Usa o endpoint **próprio** do PetBits, não o `auth/login` do template. O
    do template confere se a conta existe **antes** de comparar a senha, então
    um e-mail inexistente responde sem nunca pagar o custo do hash: o corpo da
    recusa é idêntico nos dois casos, mas o relógio não é, e isso basta para
    descobrir quem tem conta. O nosso compara sempre.

    A resposta **não traz o papel**, de propósito. Se trouxesse, a tela de
    entrada poderia decidir o destino sem o `GET /auth/me`, e aí a aba
    Colaborador conseguiria recusar sozinha — que é o oráculo de papel inteiro
    de volta.

    A mensagem de recusa é genérica: dizer "esse usuário não existe"
    permitiria descobrir quem tem conta no sistema.
    """
    try:
        return await _requisitar(
            "POST",
            "/entrar",
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


async def criar_minha_ficha(dados: dict, *, token: str) -> dict:
    """Cria a ficha de tutor da conta logada (change
    `cadastro-de-cliente-pela-conta`). O dono é o token; `dados` leva só
    documento, telefone e endereço."""
    criada = await _requisitar("POST", "/me/tutor", token=token, json=dados)
    if criada is None:
        raise XanoError("O Xano não confirmou o cadastro de cliente.")
    return criada


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


# --- área da equipe -----------------------------------------------------------
#
# Caminhos SEPARADOS dos do tutor, com prefixo `equipe/`. Não é organização de
# URL: é a decisão central desta change. Um ramo por papel dentro dos endpoints
# do tutor faria o 403 desaparecer — um tutor sondando a superfície da clínica
# receberia 200 com os dados dele, e sondar viraria tráfego normal, sem deixar
# linha nenhuma no registro do servidor.
#
# Como nos animais, o `token` é nomeado e obrigatório: esquecê-lo falha na hora
# com TypeError, em vez de sair uma requisição anônima.
#
# Nenhuma destas funções envia o papel. Quem decide se a credencial é de equipe
# é o backend, lendo o papel do banco a cada requisição.


async def painel_equipe(*, token: str) -> dict:
    """Os contadores do painel, numa requisição só.

    Existe por causa do limite de 10 requisições a cada 20 segundos, **por
    instância**: as quatro listas soltas no carregamento custariam metade do
    orçamento numa única abertura de tela, e dois colaboradores simultâneos
    derrubariam o painel e a tela dos tutores junto.

    A economia vem de juntar **recursos**, não papéis — um ramo por papel não
    pouparia requisição nenhuma, porque o painel faria as mesmas quatro
    chamadas de qualquer jeito.
    """
    dados = await _requisitar("GET", "/equipe/painel", token=token)
    return dados if isinstance(dados, dict) else {}


# --- colaboradores ---


async def listar_colaboradores(*, token: str) -> list[dict]:
    dados = await _requisitar("GET", "/equipe/colaboradores", token=token)
    return dados if isinstance(dados, list) else []


async def obter_colaborador(colaborador_id: int, *, token: str) -> Optional[dict]:
    return await _requisitar(
        "GET", f"/equipe/colaboradores/{colaborador_id}", token=token
    )


async def criar_colaborador(dados: dict, *, token: str) -> dict:
    criado = await _requisitar("POST", "/equipe/colaboradores", token=token, json=dados)
    if criado is None:
        raise XanoError("O Xano não confirmou a criação do colaborador.")
    return criado


async def atualizar_colaborador(
    colaborador_id: int, dados: dict, *, token: str
) -> dict:
    """Altera só os campos informados; os ausentes permanecem.

    Como na edição de animal, uma recusa por "não encontrado" levanta
    `NaoEncontrado` em vez de devolver None — sem isso a tela mostraria como
    salva uma alteração que o backend recusou.
    """
    atualizado = await _requisitar(
        "PATCH", f"/equipe/colaboradores/{colaborador_id}", token=token, json=dados
    )
    if atualizado is None:
        raise NaoEncontrado("Este colaborador não está mais disponível.", status=404)
    return atualizado


# --- serviços ---


async def listar_servicos(*, token: str) -> list[dict]:
    dados = await _requisitar("GET", "/equipe/servicos", token=token)
    return dados if isinstance(dados, list) else []


async def obter_servico(servico_id: int, *, token: str) -> Optional[dict]:
    return await _requisitar("GET", f"/equipe/servicos/{servico_id}", token=token)


async def criar_servico(dados: dict, *, token: str) -> dict:
    criado = await _requisitar("POST", "/equipe/servicos", token=token, json=dados)
    if criado is None:
        raise XanoError("O Xano não confirmou a criação do serviço.")
    return criado


async def atualizar_servico(servico_id: int, dados: dict, *, token: str) -> dict:
    atualizado = await _requisitar(
        "PATCH", f"/equipe/servicos/{servico_id}", token=token, json=dados
    )
    if atualizado is None:
        raise NaoEncontrado("Este serviço não está mais disponível.", status=404)
    return atualizado


# --- a visão da clínica ---
#
# Só leitura. A escrita de tutor e de animal pela equipe não foi desenhada
# nesta change: o padrão "prova + ação" fica mais apertado aqui, porque a
# consulta-prova da equipe não tem cláusula de dono e vira apenas "existe?".


async def listar_tutores_da_clinica(*, token: str) -> list[dict]:
    """Todos os tutores, inclusive os de balcão, que não têm conta de acesso.

    Esta lista leva documento, telefone e endereço. É o requisito — a recepção
    precisa disso —, mas significa que uma credencial de equipe comprometida é
    a base de clientes inteira.
    """
    dados = await _requisitar("GET", "/equipe/tutores", token=token)
    return dados if isinstance(dados, list) else []


async def listar_animais_da_clinica(*, token: str) -> list[dict]:
    """Todos os animais, com o tutor responsável de cada um.

    Inclui o animal sem tutor válido: para o tutor ele é invisível por
    construção, mas esconder da clínica um registro quebrado é pior do que
    mostrá-lo.
    """
    dados = await _requisitar("GET", "/equipe/animais", token=token)
    return dados if isinstance(dados, list) else []


# --- agendamento (change `agendamento`) ----------------------------------------
#
# Do lado do tutor, a tela só **sugere** horários: quem decide é o
# `POST agendamentos`, que refaz no Xano a conta inteira — posse, expediente,
# grade, profissional livre (design.md da change, D2).


async def listar_servicos_agendaveis(*, token: str) -> list[dict]:
    """O catálogo que o tutor vê: só serviços com categoria."""
    dados = await _requisitar("GET", "/servicos", token=token)
    return dados if isinstance(dados, list) else []


async def ocupacao_do_dia(servico_id: int, dia_ms: int, *, token: str) -> dict:
    """Profissionais compatíveis e intervalos ocupados de um dia.

    `dia_ms` é a meia-noite de São Paulo daquele dia, em ms UTC.
    """
    dados = await _requisitar(
        "GET",
        "/agenda/ocupacao",
        token=token,
        params={"servico_id": servico_id, "dia": dia_ms},
    )
    return dados if isinstance(dados, dict) else {}


async def listar_agendamentos(*, token: str) -> list[dict]:
    """Os agendamentos dos animais do tutor, do mais recente para o mais antigo."""
    dados = await _requisitar("GET", "/agendamentos", token=token)
    return dados if isinstance(dados, list) else []


async def criar_agendamento(dados: dict, *, token: str) -> dict:
    """Marca um agendamento. O profissional é escolhido pelo backend."""
    criado = await _requisitar("POST", "/agendamentos", token=token, json=dados)
    if criado is None:
        raise XanoError("O Xano não confirmou o agendamento.")
    return criado


async def cancelar_agendamento(agendamento_id: int, *, token: str) -> dict:
    """Cancela um agendamento do tutor, até 24 h antes.

    Agendamento alheio e inexistente chegam iguais, como 404 — e o 404 vira
    `NaoEncontrado` aqui, pelo mesmo motivo da edição de animal: devolver None
    deixaria a tela mostrar como cancelado o que o backend recusou.
    """
    cancelado = await _requisitar(
        "POST", f"/agendamentos/{agendamento_id}/cancelar", token=token
    )
    if cancelado is None:
        raise NaoEncontrado("Este agendamento não está mais disponível.", status=404)
    return cancelado


async def agenda_da_clinica(dia_ms: int, *, token: str) -> list[dict]:
    """A agenda de um dia, para a equipe. Só leitura."""
    dados = await _requisitar(
        "GET", "/equipe/agenda", token=token, params={"dia": dia_ms}
    )
    return dados if isinstance(dados, list) else []
