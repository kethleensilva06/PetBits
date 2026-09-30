"""Sessão do usuário: login, cadastro e o papel de quem está logado.

A sessão precisa sobreviver a um F5 e a um restart do servidor de
desenvolvimento. Uma var de estado comum não serve: o token que o Reflex usa
para reconhecer o navegador vive em `sessionStorage` e o estado do backend se
perde a cada reinício. Por isso o token e o perfil ficam em `rx.LocalStorage`,
que o navegador devolve antes mesmo dos `on_load` rodarem.

O papel guardado aqui serve para **esconder botão**, nunca para proteger dado:
qualquer pessoa edita o localStorage pelo DevTools. Quem protege é o Xano.
"""

from typing import Optional

import reflex as rx

from petbits import xano
from petbits.xano import SessaoExpirada, XanoError

# Espelha os filtros da coluna `password` da tabela user no Xano
# (min:8|minAlpha:1|minDigit:1). Validar aqui é o que permite mostrar a
# mensagem em português, em vez do erro cru do Xano.
SENHA_MINIMA = 8


def _senha_fraca(senha: str) -> Optional[str]:
    """Devolve o motivo de a senha não servir, ou None se estiver boa."""
    if len(senha) < SENHA_MINIMA:
        return f"A senha precisa ter pelo menos {SENHA_MINIMA} caracteres."
    if not any(c.isalpha() for c in senha):
        return "A senha precisa ter pelo menos uma letra."
    if not any(c.isdigit() for c in senha):
        return "A senha precisa ter pelo menos um número."
    return None


class AuthState(rx.State):
    # --- sessão: sobrevive ao F5, à aba nova e ao restart do servidor ---
    token: str = rx.LocalStorage("", name="petbits_token", sync=True)
    usuario_id: str = rx.LocalStorage("", name="petbits_usuario_id", sync=True)
    usuario_nome: str = rx.LocalStorage("", name="petbits_nome", sync=True)
    usuario_papel: str = rx.LocalStorage("", name="petbits_papel", sync=True)

    # Deliberadamente NÃO persistido. Quando o backend não lembra mais deste
    # cliente (aba nova, servidor reiniciado), isto volta a False e forçamos
    # uma revalidação no Xano. Sem essa var, todo carregamento de página
    # gastaria uma requisição com `auth/me` — e o painel já gasta sete.
    sessao_validada: bool = False

    # Por que uma var e não `/login?expirou=1`: o redirect acontece dentro da
    # mesma sessão do backend, então o estado sobrevive à troca de página — e
    # ler query string exigiria `router.page.params`, deprecado no Reflex 0.9.
    sessao_expirou: bool = False

    login_email: str = ""
    login_senha: str = ""

    cad_nome: str = ""
    cad_email: str = ""
    cad_senha: str = ""
    cad_confirmar: str = ""
    cad_cpf: str = ""
    cad_telefone: str = ""
    cad_endereco: str = ""

    auth_error: str = ""
    enviando: bool = False
    mostrar_senha: bool = False

    def set_login_email(self, value: str):
        self.login_email = value

    def set_login_senha(self, value: str):
        self.login_senha = value

    def set_cad_nome(self, value: str):
        self.cad_nome = value

    def set_cad_email(self, value: str):
        self.cad_email = value

    def set_cad_senha(self, value: str):
        self.cad_senha = value

    def set_cad_confirmar(self, value: str):
        self.cad_confirmar = value

    def set_cad_cpf(self, value: str):
        self.cad_cpf = value

    def set_cad_telefone(self, value: str):
        self.cad_telefone = value

    def set_cad_endereco(self, value: str):
        self.cad_endereco = value

    def alternar_senha(self):
        self.mostrar_senha = not self.mostrar_senha

    @rx.var
    def autenticado(self) -> bool:
        return bool(self.token)

    @rx.var
    def eh_admin(self) -> bool:
        return self.usuario_papel == "admin"

    @rx.var
    def eh_cliente(self) -> bool:
        return bool(self.token) and self.usuario_papel == "member"

    @rx.var
    def rota_inicial(self) -> str:
        """Para onde mandar a pessoa depois de entrar."""
        return "/" if self.usuario_papel == "admin" else "/portal"

    @rx.var
    def primeiro_nome(self) -> str:
        return self.usuario_nome.split(" ")[0] if self.usuario_nome else ""

    @rx.var
    def iniciais(self) -> str:
        partes = [p for p in self.usuario_nome.split(" ") if p]
        if not partes:
            return "?"
        return (partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")).upper()

    def _guardar(self, token: str, perfil: dict):
        self.token = token
        self.usuario_id = str(perfil.get("id") or "")
        self.usuario_nome = perfil.get("name") or ""
        self.usuario_papel = perfil.get("role") or "member"
        self.sessao_validada = True
        self.sessao_expirou = False

    def _limpar(self, *, expirou: bool = False):
        """Privado de propósito: método com `_` não vira event handler.

        `expirou=True` distingue "o token venceu" de "a pessoa clicou em
        Sair" — só o primeiro merece aviso na tela de login.
        """
        self.token = ""
        self.usuario_id = ""
        self.usuario_nome = ""
        self.usuario_papel = ""
        self.sessao_validada = False
        self.sessao_expirou = expirou

    async def entrar(self):
        self.auth_error = ""
        if not self.login_email.strip() or not self.login_senha:
            self.auth_error = "Informe e-mail e senha."
            return
        self.enviando = True
        yield

        try:
            sessao = await xano.entrar(self.login_email.strip(), self.login_senha)
            perfil = await xano.usuario_atual(sessao["authToken"])
        except XanoError as erro:
            self.enviando = False
            self.auth_error = str(erro)
            return

        self._guardar(sessao["authToken"], perfil)
        self.login_senha = ""
        self.enviando = False
        yield rx.redirect(self.rota_inicial)

    async def cadastrar(self):
        self.auth_error = ""
        if not self.cad_nome.strip():
            self.auth_error = "Informe seu nome."
            return
        if "@" not in self.cad_email:
            self.auth_error = "Informe um e-mail válido."
            return
        if len([c for c in self.cad_cpf if c.isdigit()]) != 11:
            self.auth_error = "O CPF precisa ter 11 dígitos."
            return
        motivo = _senha_fraca(self.cad_senha)
        if motivo:
            self.auth_error = motivo
            return
        if self.cad_senha != self.cad_confirmar:
            self.auth_error = "As senhas não são iguais."
            return

        self.enviando = True
        yield

        try:
            sessao = await xano.cadastrar_tutor(
                nome=self.cad_nome.strip(),
                email=self.cad_email.strip().lower(),
                senha=self.cad_senha,
                cpf=self.cad_cpf.strip(),
                telefone=self.cad_telefone.strip(),
                endereco=self.cad_endereco.strip(),
            )
            perfil = await xano.usuario_atual(sessao["authToken"])
        except XanoError as erro:
            self.enviando = False
            self.auth_error = str(erro)
            return

        self._guardar(sessao["authToken"], perfil)
        self.cad_senha = ""
        self.cad_confirmar = ""
        self.enviando = False
        yield rx.redirect(self.rota_inicial)

    def sair(self):
        self._limpar()
        return rx.redirect("/login")

    async def carregar_sessao(self):
        """Primeiro `on_load` de toda página protegida.

        Revalida o token no Xano só quando o backend não lembra mais deste
        cliente. Uma falha de rede aqui **não** desloga: só o 401 desloga.
        """
        if not self.token:
            self.sessao_validada = False
            return rx.redirect("/login")
        if self.sessao_validada:
            return None
        try:
            perfil = await xano.usuario_atual(self.token)
        except SessaoExpirada:
            self._limpar(expirou=True)
            return rx.redirect("/login")
        except XanoError as erro:
            self.auth_error = str(erro)
            return None
        self._guardar(self.token, perfil)
        return None

    def redirecionar_se_logado(self):
        """`on_load` do login e do cadastro: quem já entrou não vê a porta."""
        if self.token:
            return rx.redirect(self.rota_inicial)
        return None
