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

from datetime import datetime, timezone
from typing import Optional

import reflex as rx

from petbits import xano
from petbits.states.auth_state import AuthState
from petbits.xano import FalhaDeComunicacao, SessaoExpirada, XanoError


class SemSessao(Exception):
    """Não há sessão válida. `destino` é para onde mandar a pessoa."""

    def __init__(self, destino: str = "/entrar"):
        super().__init__(destino)
        self.destino = destino


def _data_para_tela(valor) -> str:
    """Campo de data do Xano no formato do input `type="date"`.

    O Xano guarda `timestamp` em milissegundos e grava **0** quando o campo não
    foi informado — não nulo. Zero é 1970, não uma data: vira campo vazio.

    A leitura é em **UTC**, de propósito. Uma data de nascimento é uma data de
    calendário, não um instante: o Xano recebe `2022-03-15` e guarda a
    meia-noite UTC daquele dia. Lendo em hora local (UTC−3) o resultado seria
    14/03 às 21:00 — e a tela mostraria o dia errado, sempre um a menos.

    Isto **não** vale para um instante de verdade, como o horário de um
    atendimento: ali o fuso importa e a conversão tem de acontecer.
    """
    if not valor:
        return ""
    try:
        return (
            datetime.fromtimestamp(float(valor) / 1000, tz=timezone.utc)
            .date()
            .isoformat()
        )
    except (TypeError, ValueError, OverflowError, OSError):
        return ""


def _data_para_exibir(valor) -> str:
    iso = _data_para_tela(valor)
    if not iso:
        return "-"
    ano, mes, dia = iso.split("-")
    return f"{dia}/{mes}/{ano}"


def _numero_para_tela(valor) -> str:
    if valor in (None, "", 0, 0.0):
        return ""
    return str(valor)


class PetState(rx.State):
    animais: list[dict] = []
    load_error: str = ""
    carregando: bool = False

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
    def titulo_dialogo(self) -> str:
        return "Editar animal" if self.editando_id is not None else "Novo animal"

    # --- sessão -----------------------------------------------------------

    async def _token(self) -> str:
        """Token de quem está logado. Levanta `SemSessao` se não houver."""
        auth = await self.get_state(AuthState)
        if not auth.token:
            raise SemSessao()
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
        try:
            token = await self._token()
            registros = await xano.listar_animais(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            self.animais = []
            self.load_error = str(erro)
            self.carregando = False
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

    # --- formulário -------------------------------------------------------

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
