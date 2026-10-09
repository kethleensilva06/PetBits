"""Sessão do usuário: criar conta, entrar, sair e saber quem está logado.

A sessão precisa sobreviver a recarregar a página, a uma aba nova e a
reiniciar o servidor de desenvolvimento. Uma variável de estado comum não
serve para nada disso: o identificador que o Reflex usa para reconhecer o
navegador vive em `sessionStorage`, e o estado do backend se perde a cada
reinício. Por isso o token e o perfil ficam em `rx.LocalStorage`, que o
navegador devolve antes mesmo dos `on_load` rodarem.

O papel guardado aqui serve para adaptar a tela, nunca para proteger dado:
qualquer pessoa edita o armazenamento local pelo DevTools. Quem protege é o
Xano.
"""

from typing import Optional

import reflex as rx
from reflex.utils.exec import is_prod_mode

from petbits import contas_de_teste, xano
from petbits.xano import FalhaDeComunicacao, SessaoExpirada, XanoError

# Espelha os filtros da coluna `password` da tabela user no Xano
# (min:8|minAlpha:1|minDigit:1). Validar aqui é o que permite mostrar a
# mensagem em português, em vez do erro cru do backend.
SENHA_MINIMA = 8


def _senha_fraca(senha: str) -> Optional[str]:
    """O motivo de a senha não servir, ou None se estiver boa."""
    if len(senha) < SENHA_MINIMA:
        return f"A senha precisa ter pelo menos {SENHA_MINIMA} caracteres."
    if not any(c.isalpha() for c in senha):
        return "A senha precisa ter pelo menos uma letra."
    if not any(c.isdigit() for c in senha):
        return "A senha precisa ter pelo menos um número."
    return None


def _so_digitos(texto: str) -> str:
    return "".join(c for c in texto if c.isdigit())


class AuthState(rx.State):
    # --- sessão: sobrevive ao F5, à aba nova e ao restart do servidor ---
    token: str = rx.LocalStorage("", name="petbits_token", sync=True)
    usuario_nome: str = rx.LocalStorage("", name="petbits_nome", sync=True)
    usuario_papel: str = rx.LocalStorage("", name="petbits_papel", sync=True)

    # Deliberadamente NÃO persistida. Quando o backend não lembra mais deste
    # navegador (aba nova, servidor reiniciado), ela volta a False e forçamos
    # uma revalidação no Xano. Nas demais navegações, economiza uma requisição
    # por página — o que importa dentro do orçamento de 10 por 20 segundos.
    sessao_validada: bool = False

    # Por que uma var e não `?expirou=1` na URL: o redirecionamento acontece
    # dentro da mesma sessão do backend, então o estado sobrevive à troca de
    # página — e ler query string exigiria uma API deprecada no Reflex 0.9.
    sessao_expirou: bool = False

    # A aba escolhida na tela de entrada: "cliente" ou "colaborador".
    #
    # Ela existe **só** para a clínica poder dizer "entre pela aba
    # Colaborador". Não participa da verificação e **nunca é enviada ao
    # servidor** — nem no corpo, nem na query, nem em cabeçalho, nem no
    # caminho. Não é "enviada e ignorada": enquanto o backend não souber qual
    # aba foi usada, nenhuma mudança futura consegue fazer a resposta depender
    # dela.
    #
    # Se as duas abas verificassem de jeitos diferentes, descobrir quem é
    # colaborador seria tentar o mesmo e-mail nas duas e ver em qual passa.
    # Por isso as duas usam este mesmo manipulador, e não dois.
    aba: str = "cliente"

    login_email: str = ""
    login_senha: str = ""

    cad_nome: str = ""
    cad_email: str = ""
    cad_senha: str = ""
    cad_confirmar: str = ""
    cad_documento: str = ""
    cad_telefone: str = ""
    cad_endereco: str = ""

    erro: str = ""
    enviando: bool = False

    # Atalho Alt+1 da tela de entrada, só em desenvolvimento. A lista que vai
    # ao navegador tem rótulo e e-mail, **nunca** a senha: ela só sai do
    # backend quando a conta é escolhida, e aí vai para o campo do formulário,
    # como se tivesse sido digitada.
    painel_teste_aberto: bool = False
    contas_teste: list[dict[str, str]] = []
    # Qual lista está aberta: `equipe` (Alt+1) ou `clientes` (Alt+2). Fica no
    # servidor e é ela que filtra a escolha — o clique manda só o índice
    # (change `atalho-de-clientes`, D2).
    painel_teste_grupo: str = contas_de_teste.EQUIPE

    def set_aba(self, value: str | list[str]):
        """O `segmented_control` do Radix entrega `str | list[str]` — ele
        serve também para seleção múltipla, e o Reflex cobra a anotação
        correspondente. Aqui a seleção é única, então a lista é reduzida ao
        primeiro item, e vazio volta para "cliente" em vez de virar uma aba
        sem nome."""
        if isinstance(value, list):
            value = value[0] if value else "cliente"
        self.aba = value or "cliente"

    def set_login_email(self, value: str):
        self.login_email = value

    def set_login_senha(self, value: str):
        self.login_senha = value

    # --- atalho de contas de teste ---------------------------------------
    #
    # A página só monta o ouvinte de teclado fora de produção, mas esconder
    # não é proteger: o evento pode chegar pelo WebSocket na mão. Por isso os
    # dois manipuladores conferem o modo de novo e não fazem nada em produção.
    # Nenhum deles lê nem altera `aba` — uma lista diferente por aba seria a
    # primeira diferença observável entre elas.

    def tecla_na_entrada(self, tecla: str, modificadores: dict):
        """`Alt+1` abre a equipe, `Alt+2` os clientes; `Esc` fecha.

        O atalho da lista aberta fecha; o da outra troca de lista sem fechar
        (change `atalho-de-clientes`). "¡" e "™" são `Alt+1` e `Alt+2` no
        teclado do macOS.
        """
        if is_prod_mode():
            return
        if tecla == "Escape":
            self.painel_teste_aberto = False
            return
        if not modificadores.get("alt_key"):
            return
        if tecla in ("1", "¡"):
            grupo = contas_de_teste.EQUIPE
        elif tecla in ("2", "™"):
            grupo = contas_de_teste.CLIENTES
        else:
            return
        if self.painel_teste_aberto and self.painel_teste_grupo == grupo:
            self.painel_teste_aberto = False
            return
        self.painel_teste_grupo = grupo
        self.contas_teste = [
            {"rotulo": c["rotulo"], "email": c["email"]}
            for c in contas_de_teste.do_grupo(grupo)
        ]
        self.painel_teste_aberto = True

    @rx.var
    def titulo_painel_teste(self) -> str:
        if self.painel_teste_grupo == contas_de_teste.CLIENTES:
            return "Clientes de teste (Alt+2)"
        return "Equipe de teste (Alt+1)"

    def fechar_painel_teste(self):
        self.painel_teste_aberto = False

    def escolher_conta_teste(self, indice: int):
        """Preenche o formulário com a conta escolhida. Não entra: a entrada
        continua sendo o envio do formulário, pela verificação de sempre.

        O arquivo é relido aqui, em vez de guardar as senhas no estado na
        abertura — guardadas, elas iriam ao navegador junto com a lista."""
        if is_prod_mode():
            return
        # O índice vale dentro do grupo aberto, que fica no servidor (D2).
        contas = contas_de_teste.do_grupo(self.painel_teste_grupo)
        if not 0 <= indice < len(contas):
            return
        self.login_email = contas[indice]["email"]
        self.login_senha = contas[indice]["senha"]
        self.erro = ""
        self.painel_teste_aberto = False

    def set_cad_nome(self, value: str):
        self.cad_nome = value

    def set_cad_email(self, value: str):
        self.cad_email = value

    def set_cad_senha(self, value: str):
        self.cad_senha = value

    def set_cad_confirmar(self, value: str):
        self.cad_confirmar = value

    def set_cad_documento(self, value: str):
        self.cad_documento = value

    def set_cad_telefone(self, value: str):
        self.cad_telefone = value

    def set_cad_endereco(self, value: str):
        self.cad_endereco = value

    @rx.var
    def autenticado(self) -> bool:
        return bool(self.token)

    @rx.var
    def primeiro_nome(self) -> str:
        return self.usuario_nome.split(" ")[0] if self.usuario_nome else ""

    @rx.var
    def papel_exibido(self) -> str:
        return xano.papel_legivel(self.usuario_papel)

    @rx.var
    def eh_equipe(self) -> bool:
        """Serve para **desenhar** o menu, nunca para proteger dado.

        Quem editar `petbits_papel` no armazenamento local vê o menu da
        equipe e recebe 403 em cada requisição: a interface mente, o backend
        não. Isso é por desenho — a proteção real lê o papel do banco a cada
        requisição, e nenhuma tela pode substituí-la.
        """
        return xano.eh_equipe(self.usuario_papel)

    @rx.var
    def papel_indefinido(self) -> bool:
        """Conta autenticada cujo papel não é nem equipe nem tutor.

        Acontece de verdade: `role` é coluna opcional, as contas de equipe
        nascem à mão no painel do Xano, e esquecer a coluna — ou pôr
        `member` por engano, que é o outro valor válido do enum — é o erro de
        operação mais provável desta change.
        """
        return bool(self.token) and not xano.papel_conhecido(self.usuario_papel)

    # --- gestão da sessão -----------------------------------------------

    def _guardar(self, token: str, perfil: dict):
        self.token = token
        self.usuario_nome = perfil.get("name") or ""
        # O papel é guardado **cru**, como o servidor o devolveu. A versão
        # anterior fazia `or xano.PAPEL_TUTOR`, o que transformava papel
        # vazio em "tutor" silenciosamente — e uma conta de equipe criada
        # sem a coluna `role` (o erro de operação mais provável, já que
        # promover alguém acontece fora do app) caía na lista de animais e
        # lia "Nenhum animal cadastrado ainda". Vazio agora continua vazio,
        # e a tela diz isso.
        self.usuario_papel = perfil.get("role") or ""
        self.sessao_validada = True
        self.sessao_expirou = False
        self.erro = ""

    def _limpar(self, *, expirou: bool = False):
        """Privado de propósito: método com `_` não vira event handler.

        `expirou=True` distingue "a credencial venceu" de "a pessoa clicou em
        Sair" — só o primeiro merece aviso na tela de entrada.
        """
        self.token = ""
        self.usuario_nome = ""
        self.usuario_papel = ""
        self.sessao_validada = False
        self.sessao_expirou = expirou
        # O formulário também: sem isto, sair deixa o e-mail de quem saiu
        # preenchido na tela. Num computador compartilhado, a próxima pessoa
        # descobre quem usou o sistema antes dela.
        self.login_email = ""
        self.login_senha = ""
        self.aba = "cliente"
        self.erro = ""

    # --- ações ------------------------------------------------------------

    async def entrar(self):
        self.erro = ""
        if not self.login_email.strip() or not self.login_senha:
            self.erro = "Informe e-mail e senha."
            return
        self.enviando = True
        yield

        # O `finally`, e não um `enviando = False` em cada ramo: foi um ramo
        # esquecido que deixou o botão cinza para sempre. Ele cobre a recusa,
        # o erro inesperado e o sucesso pelo mesmo ponto.
        try:
            sessao = await xano.entrar(self.login_email.strip(), self.login_senha)
            perfil = await xano.usuario_atual(sessao["authToken"])
        except XanoError as erro:
            self.erro = str(erro)
            return
        finally:
            self.enviando = False

        self._guardar(sessao["authToken"], perfil)
        self.login_senha = ""
        # O destino combina o papel que o servidor devolveu em `/auth/me` com
        # a aba — e a aba só é lida AQUI, depois de a senha ser aceita
        # (change `aba-define-a-area`, D1). A aba Cliente abre a área de
        # cliente para qualquer conta; a equipe só se abre para papel de
        # equipe pela aba Colaborador. Tutor pela aba Colaborador entra em
        # silêncio na área de cliente: "esta conta não é da equipe" seria a
        # única diferença observável entre as abas, e seria o oráculo de
        # papel inteiro.
        yield rx.redirect(xano.rota_do_papel(self.usuario_papel, self.aba))

    async def cadastrar(self):
        self.erro = ""
        if not self.cad_nome.strip():
            self.erro = "Informe seu nome."
            return
        if "@" not in self.cad_email:
            self.erro = "Informe um e-mail válido."
            return
        if len(_so_digitos(self.cad_documento)) != 11:
            self.erro = "O documento precisa ter 11 dígitos."
            return
        motivo = _senha_fraca(self.cad_senha)
        if motivo:
            self.erro = motivo
            return
        if self.cad_senha != self.cad_confirmar:
            self.erro = "As senhas não são iguais."
            return

        self.enviando = True
        yield

        try:
            sessao = await xano.cadastrar_tutor(
                nome=self.cad_nome.strip(),
                email=self.cad_email.strip().lower(),
                senha=self.cad_senha,
                documento=self.cad_documento.strip(),
                telefone=self.cad_telefone.strip(),
                endereco=self.cad_endereco.strip(),
            )
            perfil = await xano.usuario_atual(sessao["authToken"])
        except XanoError as erro:
            self.erro = str(erro)
            return
        finally:
            self.enviando = False

        self._guardar(sessao["authToken"], perfil)
        self.cad_senha = ""
        self.cad_confirmar = ""
        yield rx.redirect(xano.rota_do_papel(self.usuario_papel))

    async def sair(self):
        """Encerra a sessão e **apaga os dados que já estavam na tela**.

        Limpar só o token não basta. O identificador que o Reflex usa para
        reconhecer o navegador vive em `sessionStorage` e não muda ao sair, e
        o redirecionamento é navegação de página única — o estado do cliente
        não é reconstruído. Sem apagar aqui, quem entrasse em seguida no mesmo
        navegador veria a lista de animais da pessoa anterior, com observações
        clínicas, até a primeira carga terminar.

        O import é local de propósito: `pet_state` importa este módulo, e um
        import no topo fecharia o ciclo. A consequência a carregar adiante é
        que **todo State novo que guardar dado de alguém precisa entrar aqui**
        — é uma lista que cresce, e esquecer de atualizá-la é silencioso.
        """
        from petbits.states.agenda_state import AgendaState
        from petbits.states.equipe_state import EquipeState
        from petbits.states.pet_state import PetState

        pet = await self.get_state(PetState)
        pet.limpar_dados()

        equipe = await self.get_state(EquipeState)
        equipe.limpar_dados()

        agenda = await self.get_state(AgendaState)
        agenda.limpar_dados()

        self._limpar()
        return rx.redirect("/entrar")

    # --- a guarda ---------------------------------------------------------

    async def carregar_sessao(self):
        """Primeiro `on_load` de toda rota privada.

        A barreira é o **retorno antecipado** daqui. Pôr um redirecionamento
        no `on_load` não bastaria: `rx.redirect` é evento de frontend e não
        cancela o que já está na fila do backend, então qualquer carregamento
        enfileirado depois rodaria assim mesmo e a requisição sairia.

        Revalida a credencial no Xano só quando o backend não lembra mais
        deste navegador. Uma falha de rede aqui **não** desloga: só o 401
        desloga.
        """
        if not self.token:
            self.sessao_validada = False
            return rx.redirect("/entrar")
        if self.sessao_validada:
            return None
        try:
            perfil = await xano.usuario_atual(self.token)
        except SessaoExpirada:
            self._limpar(expirou=True)
            return rx.redirect("/entrar")
        except FalhaDeComunicacao as erro:
            # A sessão permanece. Quem está sem rede não está deslogado.
            self.erro = str(erro)
            return None
        except XanoError as erro:
            self.erro = str(erro)
            return None
        self._guardar(self.token, perfil)
        return None

    def redirecionar_se_logado(self):
        """`on_load` da entrada e do cadastro: quem já entrou não vê a porta.

        Também libera o botão de envio. O `finally` de `entrar` e `cadastrar`
        não cobre o processo que morre no meio da requisição — o backend de
        desenvolvimento reinicia ao salvar um arquivo —, e o estado do Reflex
        sobrevive ao recarregamento: sem isto, um `enviando` esquecido deixa a
        porta trancada naquele navegador."""
        self.enviando = False
        if self.token:
            return rx.redirect("/")
        return None
