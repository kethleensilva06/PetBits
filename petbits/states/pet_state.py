"""Estado da tela de animais do tutor.

A guarda de acesso é o retorno antecipado de `_token()`: sem sessão, nenhuma
requisição ao Xano chega a sair. Pôr um redirecionamento no `on_load` não
bastaria — ele é evento de frontend e não cancela o que já está na fila do
backend.

Este State **não filtra nada**. Ele mostra o que o backend devolveu, e o
backend só devolve os animais de quem perguntou. Filtrar aqui daria a falsa
impressão de que a proteção mora no Python, e o dia em que alguém esquecesse o
filtro da tela os animais dos outros apareceriam — porque nunca deveriam ter
chegado ao navegador.
"""

from typing import Optional

import reflex as rx

from petbits import datas, xano
from petbits.states.auth_state import AuthState
from petbits.states.sessao import SemSessao
from petbits.xano import FalhaDeComunicacao, SessaoExpirada, XanoError


# As conversões de data moram em `petbits.datas` desde que os colaboradores
# passaram a ter data de entrada: duas cópias de uma regra de data divergem em
# silêncio. Os apelidos locais ficam para não espalhar a mudança por este
# arquivo inteiro.
_data_para_tela = datas.para_campo
_data_para_exibir = datas.para_exibir
_numero_para_tela = datas.numero_para_campo


class PetState(rx.State):
    animais: list[dict] = []
    load_error: str = ""
    carregando: bool = False
    ja_carregou: bool = False

    show_dialog: bool = False
    editando_id: Optional[int] = None
    form_error: str = ""
    salvando: bool = False

    f_nome: str = ""
    f_especie: str = ""
    f_raca: str = ""
    f_nascimento: str = ""
    f_peso: str = ""
    f_observacoes: str = ""

    # Conta de equipe sem ficha de tutor (change
    # `cadastro-de-cliente-pela-conta`). Só conta que NÃO é de tutor pergunta
    # (D4) — equipe, ou conta sem papel: conta de tutor nasce com ficha no
    # cadastro público.
    sem_ficha: bool = False
    ficha_documento: str = ""
    ficha_telefone: str = ""
    ficha_endereco: str = ""
    ficha_erro: str = ""
    ficha_enviando: bool = False

    def set_ficha_documento(self, value: str):
        self.ficha_documento = value

    def set_ficha_telefone(self, value: str):
        self.ficha_telefone = value

    def set_ficha_endereco(self, value: str):
        self.ficha_endereco = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_f_nome(self, value: str):
        self.f_nome = value

    def set_f_especie(self, value: str):
        self.f_especie = value

    def set_f_raca(self, value: str):
        self.f_raca = value

    def set_f_nascimento(self, value: str):
        self.f_nascimento = value

    def set_f_peso(self, value: str):
        self.f_peso = value

    def set_f_observacoes(self, value: str):
        self.f_observacoes = value

    @rx.var
    def tem_animais(self) -> bool:
        return len(self.animais) > 0

    @rx.var
    def mostrar_vazio(self) -> bool:
        """Só depois de carregar sem erro é que "vazio" quer dizer vazio.

        Sem esta distinção, a tela diz "Nenhum animal cadastrado ainda"
        enquanto a lista ainda está vindo — e também quando a requisição
        falhou. Um tutor com animais lê isso como se tivessem sumido.
        """
        return self.ja_carregou and not self.carregando and not self.load_error and not self.animais

    def limpar_dados(self):
        """Apaga tudo o que pertence a uma pessoa. Chamado ao sair."""
        self.animais = []
        self.load_error = ""
        self.carregando = False
        self.ja_carregou = False
        self.show_dialog = False
        self.editando_id = None
        self.form_error = ""
        self.f_nome = ""
        self.f_especie = ""
        self.f_raca = ""
        self.f_nascimento = ""
        self.f_peso = ""
        self.f_observacoes = ""
        self.sem_ficha = False
        self.ficha_documento = ""
        self.ficha_telefone = ""
        self.ficha_endereco = ""
        self.ficha_erro = ""
        self.ficha_enviando = False

    @rx.var
    def titulo_dialogo(self) -> str:
        return "Editar animal" if self.editando_id is not None else "Novo animal"

    # --- sessão -----------------------------------------------------------

    async def _token(self) -> str:
        """Token de quem está logado. Levanta `SemSessao` se não houver."""
        auth = await self.get_state(AuthState)
        if not auth.token:
            # Este State só carrega no endereço principal, cujo visitante
            # sem sessão vê a página inicial (change `porta-de-entrada`, D3).
            raise SemSessao("/boas-vindas")
        # Funcionário não usa a área de cliente (change `porta-de-entrada`,
        # D5): volta para a gerência antes de qualquer requisição.
        if xano.eh_equipe(auth.usuario_papel):
            raise SemSessao("/equipe")
        return auth.token

    async def _encerrar(self, erro: Exception):
        if isinstance(erro, SessaoExpirada):
            auth = await self.get_state(AuthState)
            auth._limpar(expirou=True)
        return rx.redirect(getattr(erro, "destino", "/entrar"))

    # --- carregar ---------------------------------------------------------

    async def carregar(self):
        self.load_error = ""
        self.carregando = True
        # Defesa em profundidade: a limpeza autoritativa é no `sair`, mas
        # zerar aqui também fecha qualquer janela em que a lista de uma
        # pessoa apareça para outra.
        self.animais = []
        try:
            token = await self._token()
            auth = await self.get_state(AuthState)
            if not xano.eh_tutor(auth.usuario_papel):
                self.sem_ficha = await xano.minha_ficha(token) is None
            else:
                self.sem_ficha = False
            registros = [] if self.sem_ficha else await xano.listar_animais(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            self.animais = []
            self.load_error = str(erro)
            self.carregando = False
            self.ja_carregou = True
            return

        self.animais = [
            {
                "id": a.get("id"),
                "nome": a.get("nome") or "-",
                "especie": a.get("especie") or "-",
                "raca": a.get("raca") or "-",
                "nascimento": _data_para_exibir(a.get("data_nascimento")),
                "peso": _numero_para_tela(a.get("peso")) or "-",
                "observacoes": a.get("observacoes") or "",
                # Guardados crus para o formulário de edição não precisar de
                # outra requisição: a tela já tem o registro em mãos.
                "_nascimento_iso": _data_para_tela(a.get("data_nascimento")),
                "_peso_cru": _numero_para_tela(a.get("peso")),
            }
            for a in registros
        ]
        self.carregando = False
        self.ja_carregou = True

    # --- formulário -------------------------------------------------------

    async def completar_cadastro(self):
        """Cria a ficha de tutor da própria conta. O backend confere o CPF e
        recusa genericamente se ele já existir (D3); aqui só a forma."""
        digitos = "".join(c for c in self.ficha_documento if c.isdigit())
        if len(digitos) != 11:
            self.ficha_erro = "O CPF precisa ter 11 dígitos."
            return
        self.ficha_erro = ""
        self.ficha_enviando = True
        yield
        try:
            token = await self._token()
            dados = {"documento": digitos}
            if self.ficha_telefone.strip():
                dados["telefone"] = self.ficha_telefone.strip()
            if self.ficha_endereco.strip():
                dados["endereco"] = self.ficha_endereco.strip()
            await xano.criar_minha_ficha(dados, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            yield await self._encerrar(erro)
            return
        except XanoError as erro:
            self.ficha_erro = str(erro)
            return
        finally:
            self.ficha_enviando = False
        self.ficha_documento = ""
        self.ficha_telefone = ""
        self.ficha_endereco = ""
        resultado = await self.carregar()
        if resultado is not None:
            yield resultado

    def novo(self):
        self.editando_id = None
        self.form_error = ""
        self.f_nome = ""
        self.f_especie = ""
        self.f_raca = ""
        self.f_nascimento = ""
        self.f_peso = ""
        self.f_observacoes = ""
        self.show_dialog = True

    def editar(self, animal: dict):
        self.editando_id = animal["id"]
        self.form_error = ""
        self.f_nome = animal["nome"]
        self.f_especie = animal["especie"]
        self.f_raca = "" if animal["raca"] == "-" else animal["raca"]
        self.f_nascimento = animal["_nascimento_iso"]
        self.f_peso = animal["_peso_cru"]
        self.f_observacoes = animal["observacoes"]
        self.show_dialog = True

    def fechar(self):
        self.show_dialog = False
        self.form_error = ""

    async def salvar(self):
        if not self.f_nome.strip():
            self.form_error = "Informe o nome do animal."
            return
        if not self.f_especie.strip():
            self.form_error = "Informe a espécie."
            return

        dados = {
            "nome": self.f_nome.strip(),
            "especie": self.f_especie.strip(),
            "raca": self.f_raca.strip(),
            "observacoes": self.f_observacoes.strip(),
        }
        if self.f_peso.strip():
            try:
                dados["peso"] = float(self.f_peso.replace(",", "."))
            except ValueError:
                self.form_error = "O peso precisa ser um número."
                return
        if self.f_nascimento.strip():
            dados["data_nascimento"] = self.f_nascimento.strip()

        self.salvando = True
        yield

        try:
            token = await self._token()
            if self.editando_id is None:
                await xano.criar_animal(dados, token=token)
            else:
                await xano.atualizar_animal(self.editando_id, dados, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.salvando = False
            yield await self._encerrar(erro)
            return
        except FalhaDeComunicacao as erro:
            self.salvando = False
            self.form_error = str(erro)
            return
        except XanoError as erro:
            self.salvando = False
            self.form_error = str(erro)
            return

        self.salvando = False
        self.show_dialog = False
        self.form_error = ""
        # `carregar` é corrotina, não gerador: o resultado dela é ou None ou um
        # redirecionamento, e só o segundo precisa ser repassado adiante.
        resultado = await self.carregar()
        if resultado is not None:
            yield resultado
