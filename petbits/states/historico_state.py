"""O histórico clínico na tela: a equipe registra e lê, o tutor lê (change
`historico-clinico`).

Dois States, um por área, cada um com a guarda da sua área — levantam antes
de qualquer requisição. As requisições são sob demanda, ao abrir o histórico
de um animal: nenhuma a mais no carregamento das listas.
"""

import reflex as rx

from petbits import agenda, xano
from petbits.historico import dia_em_ms, evolucao_do_peso, linha_do_tempo, proximo_retorno
from petbits.rotulos import FUNCAO_LEGIVEL
from petbits.states import sessao
from petbits.states.sessao import SemSessao
from petbits.xano import FalhaDeComunicacao, SessaoExpirada, XanoError

FUNCOES_CLINICAS = ("veterinario", "clinico_geral")


class HistoricoEquipeState(rx.State):
    # A linha do tempo aberta
    aberto: bool = False
    pet_id: int = 0
    pet_nome: str = ""
    itens: list[dict] = []
    # O quadro do peso (change `evolucao-do-peso`); {} sem pesagem.
    peso: dict = {}
    carregando: bool = False
    erro: str = ""

    # O formulário de registro (ou de retificação)
    form_aberto: bool = False
    profissionais: list[dict] = []
    f_colaborador: str = ""
    f_data: str = ""
    f_motivo: str = ""
    f_diagnostico: str = ""
    f_tratamento: str = ""
    f_peso: str = ""
    f_retorno: str = ""
    f_agendamento: int = 0
    f_retifica: int = 0
    f_retifica_data: str = ""
    salvando: bool = False
    form_erro: str = ""

    def set_aberto(self, v: bool):
        self.aberto = v

    def set_form_aberto(self, v: bool):
        self.form_aberto = v

    def set_f_colaborador(self, v: str):
        self.f_colaborador = v

    def set_f_data(self, v: str):
        self.f_data = v

    def set_f_motivo(self, v: str):
        self.f_motivo = v

    def set_f_diagnostico(self, v: str):
        self.f_diagnostico = v

    def set_f_tratamento(self, v: str):
        self.f_tratamento = v

    def set_f_peso(self, v: str):
        self.f_peso = v

    def set_f_retorno(self, v: str):
        self.f_retorno = v

    @rx.var
    def titulo_form(self) -> str:
        return "Retificar atendimento" if self.f_retifica else "Registrar atendimento"

    def limpar_dados(self):
        self.aberto = False
        self.form_aberto = False
        self.pet_id = 0
        self.pet_nome = ""
        self.itens = []
        self.peso = {}
        self.profissionais = []
        self.erro = ""
        self.form_erro = ""
        self._limpar_form()

    def _limpar_form(self):
        for campo in ("f_colaborador", "f_data", "f_motivo", "f_diagnostico", "f_tratamento",
                      "f_peso", "f_retorno", "f_retifica_data", "form_erro"):
            setattr(self, campo, "")
        self.f_agendamento = 0
        self.f_retifica = 0

    async def _token(self) -> str:
        from petbits.states.equipe_state import EquipeState

        equipe = await self.get_state(EquipeState)
        return await equipe._token_de_equipe()

    async def _carregar_profissionais(self, token: str):
        """Os veterinários e clínicos gerais ativos, para o "quem atendeu".
        Uma requisição, só na primeira abertura do formulário."""
        if self.profissionais:
            return
        registros = await xano.listar_colaboradores(token=token)
        self.profissionais = [
            {"id": str(c.get("id")),
             "rotulo": f"{c.get('nome') or '-'} · {FUNCAO_LEGIVEL.get(c.get('funcao'), '')}"}
            for c in registros
            if c.get("funcao") in FUNCOES_CLINICAS and c.get("ativo") is not False
        ]

    # --- a linha do tempo ---------------------------------------------------

    async def abrir(self, animal: dict):
        self.pet_id = int(animal.get("id") or 0)
        self.pet_nome = animal.get("nome") or "-"
        self.aberto = True
        return await self._recarregar()

    async def _recarregar(self):
        self.erro = ""
        self.carregando = True
        try:
            token = await self._token()
            registros = await xano.historico_na_clinica(self.pet_id, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await sessao.encerrar(self, erro)
        except XanoError as erro:
            self.erro = str(erro)
            self.carregando = False
            return
        self.itens = linha_do_tempo(registros)
        self.peso = evolucao_do_peso(registros)
        self.carregando = False

    # --- o formulário -------------------------------------------------------

    async def _abrir_form(self):
        self.form_erro = ""
        try:
            token = await self._token()
            await self._carregar_profissionais(token)
        except (SemSessao, SessaoExpirada) as erro:
            return await sessao.encerrar(self, erro)
        except XanoError as erro:
            self.form_erro = str(erro)
        self.form_aberto = True

    async def novo(self):
        """Pela linha do tempo do animal: vale para emergência, sem agendamento."""
        self._limpar_form()
        from petbits import agenda

        self.f_data = agenda.hoje().isoformat()
        return await self._abrir_form()

    async def retificar(self, item: dict):
        """Abre o formulário com os dados do atendimento e `retifica` dele."""
        self._limpar_form()
        from petbits import agenda

        self.f_retifica = int(item.get("id") or 0)
        self.f_retifica_data = item.get("data") or ""
        self.f_colaborador = str(item.get("_id_colaborador") or "")
        self.f_data = agenda.hoje().isoformat()
        self.f_motivo = item.get("motivo") or ""
        self.f_diagnostico = item.get("diagnostico") or ""
        self.f_tratamento = item.get("tratamento") or ""
        self.f_peso = item.get("_peso") or ""
        return await self._abrir_form()

    async def da_agenda(self, agendamento: dict):
        """Pela agenda do dia: animal, profissional e agendamento preenchidos;
        registrar conclui o agendamento (D4)."""
        self._limpar_form()
        from petbits import agenda

        self.aberto = False
        self.pet_id = int(agendamento.get("_id_pet") or 0)
        self.pet_nome = agendamento.get("pet_nome") or "-"
        self.f_agendamento = int(agendamento.get("id") or 0)
        self.f_colaborador = str(agendamento.get("_id_colaborador") or "")
        self.f_data = agenda.hoje().isoformat()
        return await self._abrir_form()

    async def salvar(self):
        self.form_erro = ""
        if not self.f_colaborador:
            self.form_erro = "Escolha quem atendeu."
            return
        if not self.f_diagnostico.strip():
            self.form_erro = "O diagnóstico não pode ficar em branco."
            return
        dados = {
            "pet_id": self.pet_id,
            "id_colaborador": int(self.f_colaborador),
            "diagnostico": self.f_diagnostico.strip(),
            "motivo": self.f_motivo.strip(),
            "tratamento": self.f_tratamento.strip(),
        }
        data = dia_em_ms(self.f_data)
        if data:
            dados["data_atendimento"] = data
        retorno = dia_em_ms(self.f_retorno)
        if retorno:
            dados["retorno"] = retorno
        if self.f_peso.strip():
            try:
                dados["peso"] = float(self.f_peso.replace(",", "."))
            except ValueError:
                self.form_erro = "O peso precisa ser um número."
                return
        if self.f_agendamento:
            dados["id_agendamento"] = self.f_agendamento
        if self.f_retifica:
            dados["retifica"] = self.f_retifica

        self.salvando = True
        yield
        try:
            token = await self._token()
            await xano.registrar_atendimento(dados, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.salvando = False
            yield await sessao.encerrar(self, erro)
            return
        except (FalhaDeComunicacao, XanoError) as erro:
            self.salvando = False
            self.form_erro = str(erro)
            return
        self.salvando = False
        self.form_aberto = False
        veio_da_agenda = bool(self.f_agendamento)
        self._limpar_form()
        yield rx.toast.success("Atendimento registrado.")
        if veio_da_agenda:
            # O agendamento virou concluído: a agenda mostra isso já.
            from petbits.states.equipe_state import EquipeState

            equipe = await self.get_state(EquipeState)
            resultado = await equipe.carregar_agenda()
            if resultado is not None:
                yield resultado
        else:
            resultado = await self._recarregar()
            if resultado is not None:
                yield resultado


class HistoricoTutorState(rx.State):
    """A linha do tempo de um animal do tutor, só de leitura."""

    aberto: bool = False
    pet_nome: str = ""
    itens: list[dict] = []
    # O quadro do peso (change `evolucao-do-peso`); {} sem pesagem.
    peso: dict = {}
    # O retorno sugerido e o animal, para o Agendar retorno (change
    # `agendar-retorno`); {} sem retorno de hoje em diante.
    retorno: dict = {}
    pet_id: int = 0
    carregando: bool = False
    erro: str = ""

    def set_aberto(self, v: bool):
        self.aberto = v

    async def agendar_retorno(self):
        """Fecha o histórico e abre a Agenda com o animal e a Clínica escolhidos."""
        from petbits.states.agenda_state import AgendaState

        agenda_do_tutor = await self.get_state(AgendaState)
        # Os campos direto, como o `set_categoria` faz: a categoria muda e o
        # serviço e o horário escolhidos antes saem.
        agenda_do_tutor.categoria = "clinica"
        agenda_do_tutor.servico_id = ""
        agenda_do_tutor._limpar_escolha_de_horario()
        agenda_do_tutor.pet_id = str(self.pet_id)
        self.aberto = False
        return rx.redirect("/agenda")

    def limpar_dados(self):
        self.aberto = False
        self.pet_nome = ""
        self.itens = []
        self.peso = {}
        self.carregando = False
        self.erro = ""
        self.retorno = {}
        self.pet_id = 0

    async def abrir(self, animal: dict):
        self.pet_nome = animal.get("nome") or "-"
        self.pet_id = int(animal.get("id") or 0)
        self.itens = []
        self.peso = {}
        self.retorno = {}
        self.erro = ""
        self.aberto = True
        self.carregando = True
        yield
        try:
            token = await sessao.token_de_cliente(self, sem_sessao="/")
            registros = await xano.historico_do_meu_animal(int(animal.get("id") or 0),
                                                            token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            yield await sessao.encerrar(self, erro)
            return
        except XanoError as erro:
            self.erro = str(erro)
            self.carregando = False
            return
        self.itens = linha_do_tempo(registros)
        self.peso = evolucao_do_peso(registros)
        self.retorno = proximo_retorno(registros, agenda.agora_ms())
        self.carregando = False
