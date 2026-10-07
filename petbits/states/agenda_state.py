"""Estado da agenda do tutor (change `agendamento`).

Como em `PetState`, a guarda é o retorno antecipado de `_token()`: sem
sessão, nenhuma requisição ao Xano sai.

Este State **sugere** horários a partir da ocupação que o backend devolve
(`petbits.agenda.horarios_livres`). Quem decide é o `POST agendamentos`, que
refaz a conta inteira no Xano — se a tela errar, o backend recusa e a mensagem
dele aparece aqui (design.md da change, D2).

Orçamento de requisições: abrir custa 3 (serviços, animais, agendamentos);
escolher um dia custa 1; confirmar e cancelar custam 2 cada (a ação e a lista
recarregada).
"""

from datetime import date
from typing import Any

import reflex as rx

from petbits import agenda, xano
from petbits.states.auth_state import AuthState
from petbits.states.sessao import SemSessao
from petbits.xano import SessaoExpirada, XanoError

CATEGORIAS = agenda.CATEGORIAS
SITUACOES = agenda.SITUACOES
FUNCOES = {"veterinario": "Veterinário", "clinico_geral": "Clínico geral", "tosador": "Tosador"}


def _preco(valor) -> str:
    try:
        return f"R$ {float(valor):.2f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


class AgendaState(rx.State):
    servicos: list[dict] = []
    animais: list[dict] = []
    agendamentos: list[dict] = []

    categoria: str = "clinica"
    servico_id: str = ""
    pet_id: str = ""
    observacoes: str = ""

    ano: int = 0
    mes: int = 0
    dia_iso: str = ""
    horarios: list[dict] = []
    horario_ms: int = 0

    carregando: bool = False
    ja_carregou: bool = False
    buscando_horarios: bool = False
    enviando: bool = False
    erro: str = ""
    erro_lista: str = ""
    aviso: str = ""

    # --- campos ---------------------------------------------------------

    def set_categoria(self, value: str | list[str]):
        """O `segmented_control` entrega `str | list[str]` (ver `AuthState.set_aba`)."""
        if isinstance(value, list):
            value = value[0] if value else "clinica"
        self.categoria = value or "clinica"
        self.servico_id = ""
        self._limpar_escolha_de_horario()

    def set_servico_id(self, value: str):
        self.servico_id = value
        self._limpar_escolha_de_horario()

    def set_pet_id(self, value: str):
        self.pet_id = value

    def set_observacoes(self, value: str):
        self.observacoes = value

    def _limpar_escolha_de_horario(self):
        self.dia_iso = ""
        self.horarios = []
        self.horario_ms = 0
        self.erro = ""

    # --- derivados --------------------------------------------------------

    @rx.var
    def servicos_da_categoria(self) -> list[dict]:
        return [s for s in self.servicos if s["categoria"] == self.categoria]

    @rx.var
    def servico_escolhido(self) -> dict:
        for s in self.servicos:
            if str(s["id"]) == self.servico_id:
                return s
        return {}

    @rx.var
    def titulo_do_mes(self) -> str:
        if not self.mes:
            return ""
        return f"{agenda.MESES[self.mes - 1]} {self.ano}"

    @rx.var
    def pode_voltar_mes(self) -> bool:
        atual = agenda.hoje()
        return (self.ano, self.mes) > (atual.year, atual.month)

    @rx.var
    def semanas(self) -> list[list[dict[str, Any]]]:
        """O mês para desenhar: domingo e dia passado vêm desabilitados."""
        if not self.mes:
            return []
        hoje = agenda.hoje()
        resultado = []
        for semana in agenda.semanas_do_mes(self.ano, self.mes):
            linha = []
            for dia in semana:
                if dia is None:
                    linha.append({"iso": "", "numero": "", "habilitado": False, "escolhido": False})
                    continue
                linha.append({
                    "iso": dia.isoformat(),
                    "numero": str(dia.day),
                    "habilitado": agenda.abre(dia) and dia >= hoje,
                    "escolhido": dia.isoformat() == self.dia_iso,
                })
            resultado.append(linha)
        return resultado

    @rx.var
    def dia_por_extenso(self) -> str:
        return agenda.data_por_extenso(date.fromisoformat(self.dia_iso)) if self.dia_iso else ""

    @rx.var
    def resumo(self) -> str:
        """O que vai ser marcado, numa frase, antes de confirmar."""
        if not (self.horario_ms and self.servico_id and self.pet_id):
            return ""
        animal = next((a["nome"] for a in self.animais if str(a["id"]) == self.pet_id), "")
        return (
            f"{self.servico_escolhido.get('nome', '')} para {animal}, "
            f"{agenda.data_curta(self.horario_ms)} às {agenda.hora(self.horario_ms)}"
        )

    @rx.var
    def tem_agendamentos(self) -> bool:
        return len(self.agendamentos) > 0

    def limpar_dados(self):
        """Apaga tudo o que pertence a uma pessoa. Chamado pelo `sair`."""
        self.servicos = []
        self.animais = []
        self.agendamentos = []
        self.categoria = "clinica"
        self.servico_id = ""
        self.pet_id = ""
        self.observacoes = ""
        self.ano = 0
        self.mes = 0
        self._limpar_escolha_de_horario()
        self.carregando = False
        self.ja_carregou = False
        self.buscando_horarios = False
        self.enviando = False
        self.erro_lista = ""
        self.aviso = ""

    # --- sessão -----------------------------------------------------------

    async def _token(self) -> str:
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
        self.erro = ""
        self.erro_lista = ""
        self.aviso = ""
        self.carregando = True
        # Defesa em profundidade, como em `PetState.carregar`: nada de uma
        # pessoa fica na tela enquanto a lista de outra está vindo.
        self.servicos = []
        self.animais = []
        self.agendamentos = []
        if not self.mes:
            atual = agenda.hoje()
            self.ano, self.mes = atual.year, atual.month
        try:
            token = await self._token()
            servicos = await xano.listar_servicos_agendaveis(token=token)
            animais = await xano.listar_animais(token=token)
            agendamentos = await xano.listar_agendamentos(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            self.erro_lista = str(erro)
            self.carregando = False
            self.ja_carregou = True
            return

        self.servicos = [
            {
                "id": s.get("id"),
                "nome": s.get("nome") or "-",
                "descricao": s.get("descricao") or "",
                "categoria": s.get("categoria") or "",
                "duracao": int(s.get("duracao_minutos") or 0),
                "preco": _preco(s.get("preco")),
            }
            for s in servicos
        ]
        self.animais = [{"id": a.get("id"), "nome": a.get("nome") or "-"} for a in animais]
        if len(self.animais) == 1:
            self.pet_id = str(self.animais[0]["id"])
        self._guardar_agendamentos(agendamentos)
        self.carregando = False
        self.ja_carregou = True

    def _guardar_agendamentos(self, registros: list[dict]):
        agora = agenda.agora_ms()
        self.agendamentos = [
            {
                "id": a.get("id"),
                "quando": f"{agenda.data_curta(a.get('inicio'))}, "
                          f"{agenda.hora(a.get('inicio'))}–{agenda.hora(a.get('fim'))}",
                "animal": a.get("pet_nome") or "-",
                "servico": a.get("servico_nome") or "-",
                "categoria": CATEGORIAS.get(a.get("servico_categoria") or "", ""),
                "profissional": " · ".join(filter(None, [
                    a.get("profissional_nome") or "",
                    FUNCOES.get(a.get("profissional_funcao") or "", ""),
                ])) or "-",
                "situacao": SITUACOES.get(a.get("situacao") or "", "-"),
                "cancelado": a.get("situacao") == "cancelado",
                # O botão só aparece quando o backend aceitaria. Se o relógio
                # da máquina divergir do Xano, a recusa dele aparece na tela.
                "pode_cancelar": a.get("situacao") == "marcado"
                                 and agenda.pode_cancelar(int(a.get("inicio") or 0), agora),
                "dentro_do_prazo": a.get("situacao") == "marcado"
                                   and int(a.get("inicio") or 0) > agora
                                   and not agenda.pode_cancelar(int(a.get("inicio") or 0), agora),
            }
            for a in registros
        ]

    # --- calendário --------------------------------------------------------

    def mes_anterior(self):
        if self.pode_voltar_mes:
            self.ano, self.mes = agenda.mes_vizinho(self.ano, self.mes, -1)

    def mes_seguinte(self):
        self.ano, self.mes = agenda.mes_vizinho(self.ano, self.mes, 1)

    async def escolher_dia(self, iso: str):
        self.aviso = ""
        if not iso:
            return
        if not self.servico_id:
            self.erro = "Escolha o serviço antes do dia."
            return
        self.dia_iso = iso
        self.horarios = []
        self.horario_ms = 0
        self.erro = ""
        self.buscando_horarios = True
        yield

        dia = date.fromisoformat(iso)
        try:
            token = await self._token()
            dados = await xano.ocupacao_do_dia(
                int(self.servico_id), agenda.inicio_do_dia_ms(dia), token=token
            )
        except (SemSessao, SessaoExpirada) as erro:
            self.buscando_horarios = False
            yield await self._encerrar(erro)
            return
        except XanoError as erro:
            self.erro = str(erro)
            self.buscando_horarios = False
            return

        profissionais = [int(p["id"]) for p in dados.get("profissionais") or []]
        livres = agenda.horarios_livres(
            dia,
            self.servico_escolhido.get("duracao", 0),
            profissionais,
            dados.get("ocupados") or [],
            agenda.agora_ms(),
        )
        self.horarios = [{"ms": ms, "rotulo": agenda.hora(ms)} for ms in livres]
        self.buscando_horarios = False

    def escolher_horario(self, ms: int):
        self.horario_ms = ms
        self.erro = ""

    # --- ações --------------------------------------------------------------

    async def confirmar(self):
        self.aviso = ""
        if not self.pet_id:
            self.erro = "Escolha o animal."
            return
        if not self.servico_id:
            self.erro = "Escolha o serviço."
            return
        if not self.horario_ms:
            self.erro = "Escolha o dia e o horário."
            return
        self.erro = ""
        self.enviando = True
        yield

        try:
            token = await self._token()
            dados = {
                "pet_id": int(self.pet_id),
                "servico_id": int(self.servico_id),
                "inicio": self.horario_ms,
            }
            if self.observacoes.strip():
                dados["observacoes"] = self.observacoes.strip()
            await xano.criar_agendamento(dados, token=token)
            registros = await xano.listar_agendamentos(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            yield await self._encerrar(erro)
            return
        except XanoError as erro:
            self.erro = str(erro)
            return
        finally:
            # Mesmo motivo da change `entrada-sem-trava`: o botão volta em
            # qualquer saída, e não só nos caminhos previstos.
            self.enviando = False

        self.aviso = f"Agendado: {self.resumo}."
        self.observacoes = ""
        self._limpar_escolha_de_horario()
        self._guardar_agendamentos(registros)

    async def cancelar(self, agendamento_id: int):
        self.aviso = ""
        self.erro_lista = ""
        try:
            token = await self._token()
            await xano.cancelar_agendamento(agendamento_id, token=token)
            registros = await xano.listar_agendamentos(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.erro_lista = str(erro)
            return
        self._guardar_agendamentos(registros)
        self.aviso = "Agendamento cancelado. O horário voltou a ficar livre."
