"""Meu perfil: os dados do tutor, a troca de senha e a foto (change `perfil-e-fotos`).

Mesma guarda da área de cliente (`sessao.token_de_cliente`): sem sessão, ou
com conta de equipe, levanta antes de qualquer requisição. A ficha alterada é
sempre a do token — o backend nem aceita CPF ou e-mail neste caminho.
"""

import reflex as rx

from petbits import xano
from petbits.fotos_enviadas import FotoRecusada, extensao_da_foto, url_da_foto
from petbits.states import sessao
from petbits.states.auth_state import AuthState
from petbits.states.sessao import SemSessao
from petbits.xano import FalhaDeComunicacao, SessaoExpirada, XanoError

ID_UPLOAD = "foto_de_perfil"


class PerfilState(rx.State):
    carregando: bool = False
    ja_carregou: bool = False
    erro: str = ""

    nome: str = ""
    telefone: str = ""
    endereco: str = ""
    documento: str = ""
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
        self.telefone = v

    def set_endereco(self, v: str):
        self.endereco = v

    def set_senha_atual(self, v: str):
        self.senha_atual = v

    def set_nova_senha(self, v: str):
        self.nova_senha = v

    def set_confirmar(self, v: str):
        self.confirmar = v

    @rx.var
    def iniciais(self) -> str:
        partes = [p for p in self.nome.split() if p[:1].isalpha()]
        return "".join(p[0] for p in partes[:2]).upper() or "?"

    def limpar_dados(self):
        """Apaga tudo o que pertence a uma pessoa. Chamado pelo `sair`."""
        for campo in ("erro", "nome", "telefone", "endereco", "documento", "email",
                      "foto_url", "aviso_dados", "erro_dados", "senha_atual", "nova_senha",
                      "confirmar", "aviso_senha", "erro_senha", "erro_foto"):
            setattr(self, campo, "")
        self.carregando = False
        self.ja_carregou = False
        self.salvando = False
        self.trocando = False
        self.enviando_foto = False

    async def _token(self) -> str:
        return await sessao.token_de_cliente(self)

    def _preencher(self, ficha: dict):
        self.nome = ficha.get("nome") or ""
        self.telefone = ficha.get("telefone") or ""
        self.endereco = ficha.get("endereco") or ""
        self.documento = ficha.get("documento") or ""
        self.email = ficha.get("email") or ""
        self.foto_url = url_da_foto(ficha.get("foto"))

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
            ficha = await xano.minha_ficha(token)
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
            self.erro = "Esta conta não tem ficha de tutor. Procure a clínica."
            return
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
            ficha = await xano.alterar_minha_ficha(
                {"nome": self.nome.strip(), "telefone": self.telefone.strip(),
                 "endereco": self.endereco.strip()},
                token=token,
            )
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
        # O nome do cabeçalho ("Olá, Ana!") vem do AuthState; sem isto ele
        # ficaria com o nome antigo até a próxima entrada.
        auth = await self.get_state(AuthState)
        auth.usuario_nome = self.nome
        self.aviso_dados = "Dados atualizados."

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
        self.aviso_senha = "Senha alterada. Use a nova na próxima entrada."

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
            foto = await xano.enviar_foto_de_perfil(conteudo, extensao, token=token)
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
        yield rx.clear_selected_files(ID_UPLOAD)
