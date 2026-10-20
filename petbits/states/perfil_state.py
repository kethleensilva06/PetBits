"""Meu perfil: os dados, a troca de senha e a foto — do tutor e de quem é da equipe.

O tutor veio na change `perfil-e-fotos`; a equipe, na `perfil-do-colaborador`.
As duas telas fazem a mesma coisa sobre fichas diferentes, então o que é comum
mora em `_PerfilBase` (um mixin: cada State concreto tem as suas variáveis, e
um não enxerga o que o outro carregou). Cada um diz só de onde lê, onde grava
e para onde manda a foto.

A guarda é a de cada área (`sessao.token_de_cliente` ou a de equipe): sem a
conta certa, levanta antes de qualquer requisição. A ficha alterada é sempre a
do token — o backend nem aceita CPF, e-mail ou função neste caminho.
"""

import reflex as rx

from petbits import datas, mascaras, xano
from petbits.fotos_enviadas import FotoRecusada, extensao_da_foto, url_da_foto
from petbits.rotulos import FUNCAO_LEGIVEL
from petbits.states import sessao
from petbits.states.auth_state import AuthState
from petbits.states.sessao import SemSessao
from petbits.xano import FalhaDeComunicacao, SessaoExpirada, XanoError

ID_UPLOAD = "foto_de_perfil"
ID_UPLOAD_EQUIPE = "foto_de_perfil_equipe"


class _PerfilBase(rx.State, mixin=True):
    carregando: bool = False
    ja_carregou: bool = False
    erro: str = ""
    # Conta de equipe sem ficha com o mesmo e-mail: a tela mostra só a senha
    # e o aviso (change `perfil-do-colaborador`, D1).
    tem_ficha: bool = True

    nome: str = ""
    telefone: str = ""
    email: str = ""
    foto_url: str = ""

    salvando: bool = False
    aviso_dados: str = ""
    erro_dados: str = ""

    senha_atual: str = ""
    nova_senha: str = ""
    confirmar: str = ""
    trocando: bool = False
    aviso_senha: str = ""
    erro_senha: str = ""

    enviando_foto: bool = False
    erro_foto: str = ""

    def set_nome(self, v: str):
        self.nome = v

    def set_telefone(self, v: str):
        # Formatado a cada tecla (change `acabamentos-de-tela`, D5).
        self.telefone = mascaras.telefone(v)

    def set_senha_atual(self, v: str):
        self.senha_atual = v

    def set_nova_senha(self, v: str):
        self.nova_senha = v

    def set_confirmar(self, v: str):
        self.confirmar = v

    @rx.var
    def iniciais(self) -> str:
        partes = [p for p in self.nome.split()
                  if p[:1].isalpha() and p.lower().rstrip(".") not in ("dr", "dra", "sr", "sra")]
        return "".join(p[0] for p in partes[:2]).upper() or "?"

    # Textos que pertencem a uma pessoa; cada área acrescenta os seus.
    _TEXTOS = ("erro", "nome", "telefone", "email", "foto_url", "aviso_dados", "erro_dados",
               "senha_atual", "nova_senha", "confirmar", "aviso_senha", "erro_senha",
               "erro_foto")

    def _textos_da_area(self) -> tuple:
        return ()

    def preparar_carga(self):
        """Primeiro evento do `on_load` (change `esqueletos-de-carregamento`).

        O carregador só manda o estado à tela quando termina; sem este passo,
        o "carregando" nunca chegava, e a tela mostrava o vazio até os dados
        virem. Sem requisição: só avisa a tela de que a carga começou.
        """
        self.erro = ""
        self.carregando = True
        self.ja_carregou = False

    def limpar_dados(self):
        """Apaga tudo o que pertence a uma pessoa. Chamado pelo `sair`."""
        for campo in self._TEXTOS + self._textos_da_area():
            setattr(self, campo, "")
        self.carregando = False
        self.ja_carregou = False
        self.tem_ficha = True
        self.salvando = False
        self.trocando = False
        self.enviando_foto = False

    # --- o que cada área diz ---------------------------------------------

    async def _token(self) -> str:
        raise NotImplementedError

    async def _ler(self, token: str) -> dict | None:
        """A ficha, ou None quando a conta não tem ficha."""
        raise NotImplementedError

    def _preencher(self, ficha: dict):
        raise NotImplementedError

    def _dados_para_gravar(self) -> dict:
        raise NotImplementedError

    async def _gravar(self, dados: dict, token: str) -> dict:
        raise NotImplementedError

    async def _gravar_foto(self, conteudo: bytes, extensao: str, token: str) -> dict:
        raise NotImplementedError

    def _id_upload(self) -> str:
        raise NotImplementedError

    def _sem_ficha(self):
        raise NotImplementedError

    # --- comum ------------------------------------------------------------

    async def _guardar_foto_no_cabecalho(self):
        auth = await self.get_state(AuthState)
        auth.usuario_foto = self.foto_url

    async def carregar(self):
        # Avisos de uma visita anterior não valem para esta: um "A foto pode ter
        # no máximo 5 MB" de ontem, ainda na tela, parece erro de agora.
        for campo in ("erro", "aviso_dados", "erro_dados", "aviso_senha", "erro_senha",
                      "erro_foto", "senha_atual", "nova_senha", "confirmar"):
            setattr(self, campo, "")
        self.carregando = True
        try:
            token = await self._token()
            ficha = await self._ler(token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await sessao.encerrar(self, erro)
        except XanoError as erro:
            self.erro = str(erro)
            self.carregando = False
            return
        self.carregando = False
        self.ja_carregou = True
        if not ficha:
            self._sem_ficha()
            return
        self.tem_ficha = True
        self._preencher(ficha)
        await self._guardar_foto_no_cabecalho()

    async def salvar_dados(self):
        self.aviso_dados = ""
        self.erro_dados = ""
        if not self.nome.strip():
            self.erro_dados = "O nome não pode ficar em branco."
            return
        self.salvando = True
        yield
        try:
            token = await self._token()
            ficha = await self._gravar(self._dados_para_gravar(), token)
        except (SemSessao, SessaoExpirada) as erro:
            self.salvando = False
            yield await sessao.encerrar(self, erro)
            return
        except (FalhaDeComunicacao, XanoError) as erro:
            self.salvando = False
            self.erro_dados = str(erro)
            return
        self.salvando = False
        self._preencher(ficha)
        # O backend também muda o nome da conta (change `perfil-do-colaborador`,
        # D3 e D4); aqui é só para o topo mostrar já, sem esperar a próxima entrada.
        auth = await self.get_state(AuthState)
        auth.usuario_nome = self.nome
        # Notificação que some sozinha (change `acabamentos-de-tela`, D2).
        yield rx.toast.success("Dados atualizados.")

    async def trocar_senha(self):
        self.aviso_senha = ""
        self.erro_senha = ""
        if not self.senha_atual or not self.nova_senha:
            self.erro_senha = "Informe a senha atual e a nova."
            return
        if self.nova_senha != self.confirmar:
            self.erro_senha = "A nova senha e a confirmação não conferem."
            return
        nova = self.nova_senha
        if len(nova) < 8 or not any(c.isalpha() for c in nova) or not any(c.isdigit() for c in nova):
            self.erro_senha = "A senha precisa de pelo menos 8 caracteres, com uma letra e um número."
            return
        self.trocando = True
        yield
        try:
            token = await self._token()
            await xano.trocar_senha(self.senha_atual, nova, self.confirmar, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.trocando = False
            yield await sessao.encerrar(self, erro)
            return
        except (FalhaDeComunicacao, XanoError) as erro:
            self.trocando = False
            self.erro_senha = str(erro)
            return
        self.trocando = False
        self.senha_atual = ""
        self.nova_senha = ""
        self.confirmar = ""
        yield rx.toast.success("Senha alterada. Use a nova na próxima entrada.")

    async def enviar_foto(self, arquivos: list[rx.UploadFile]):
        self.erro_foto = ""
        if not arquivos:
            return
        arquivo = arquivos[0]
        conteudo = await arquivo.read()
        try:
            extensao = extensao_da_foto(arquivo.name, len(conteudo))
        except FotoRecusada as motivo:
            self.erro_foto = str(motivo)
            return
        self.enviando_foto = True
        yield
        try:
            token = await self._token()
            foto = await self._gravar_foto(conteudo, extensao, token)
        except (SemSessao, SessaoExpirada) as erro:
            self.enviando_foto = False
            yield await sessao.encerrar(self, erro)
            return
        except (FalhaDeComunicacao, XanoError) as erro:
            self.enviando_foto = False
            self.erro_foto = str(erro)
            return
        self.enviando_foto = False
        self.foto_url = url_da_foto(foto)
        await self._guardar_foto_no_cabecalho()
        yield rx.clear_selected_files(self._id_upload())
        yield rx.toast.success("Foto atualizada.")


class PerfilState(_PerfilBase, rx.State):
    """O perfil do tutor (change `perfil-e-fotos`)."""

    endereco: str = ""
    documento: str = ""

    def set_endereco(self, v: str):
        self.endereco = v

    def _textos_da_area(self) -> tuple:
        return ("endereco", "documento")

    async def _token(self) -> str:
        return await sessao.token_de_cliente(self)

    async def _ler(self, token: str) -> dict | None:
        return await xano.minha_ficha(token)

    def _preencher(self, ficha: dict):
        self.nome = ficha.get("nome") or ""
        self.telefone = mascaras.telefone(ficha.get("telefone"))
        self.endereco = ficha.get("endereco") or ""
        self.documento = mascaras.cpf(ficha.get("documento"))
        self.email = ficha.get("email") or ""
        self.foto_url = url_da_foto(ficha.get("foto"))

    def _dados_para_gravar(self) -> dict:
        return {"nome": self.nome.strip(), "telefone": self.telefone.strip(),
                "endereco": self.endereco.strip()}

    async def _gravar(self, dados: dict, token: str) -> dict:
        return await xano.alterar_minha_ficha(dados, token=token)

    async def _gravar_foto(self, conteudo: bytes, extensao: str, token: str) -> dict:
        return await xano.enviar_foto_de_perfil(conteudo, extensao, token=token)

    def _id_upload(self) -> str:
        return ID_UPLOAD

    def _sem_ficha(self):
        self.erro = "Esta conta não tem ficha de tutor. Procure a clínica."


class PerfilEquipeState(_PerfilBase, rx.State):
    """O perfil de quem é da equipe (change `perfil-do-colaborador`).

    A ficha é a de colaborador com o mesmo e-mail da conta (D1). Função, e-mail
    e data de entrada aparecem travados: quem define é a gerência.
    """

    funcao: str = ""
    data_entrada: str = ""

    def _textos_da_area(self) -> tuple:
        return ("funcao", "data_entrada")

    async def _token(self) -> str:
        auth = await self.get_state(AuthState)
        if not auth.token:
            raise SemSessao("/entrar")
        if not xano.eh_equipe(auth.usuario_papel):
            raise SemSessao("/")
        return auth.token

    async def _ler(self, token: str) -> dict | None:
        resposta = await xano.meu_perfil_de_equipe(token=token)
        conta = resposta.get("conta") or {}
        # Sem ficha, o nome e o e-mail da conta ainda servem ao avatar e à tela.
        self.nome = conta.get("nome") or ""
        self.email = conta.get("email") or ""
        return resposta.get("ficha")

    def _preencher(self, ficha: dict):
        self.nome = ficha.get("nome") or ""
        self.telefone = mascaras.telefone(ficha.get("telefone"))
        self.email = ficha.get("email") or self.email
        self.funcao = FUNCAO_LEGIVEL.get(ficha.get("funcao") or "", ficha.get("funcao") or "")
        self.data_entrada = datas.para_exibir(ficha.get("data_entrada"))
        self.foto_url = url_da_foto(ficha.get("foto"))

    def _dados_para_gravar(self) -> dict:
        return {"nome": self.nome.strip(), "telefone": self.telefone.strip()}

    async def _gravar(self, dados: dict, token: str) -> dict:
        return await xano.alterar_meu_perfil_de_equipe(dados, token=token)

    async def _gravar_foto(self, conteudo: bytes, extensao: str, token: str) -> dict:
        return await xano.enviar_minha_foto_de_equipe(conteudo, extensao, token=token)

    def _id_upload(self) -> str:
        return ID_UPLOAD_EQUIPE

    def _sem_ficha(self):
        self.tem_ficha = False
        self.foto_url = ""

