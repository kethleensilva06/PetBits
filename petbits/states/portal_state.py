"""Estado do portal do tutor.

**Um State só para as seis telas**, e não um por página, por duas razões:

1. *Orçamento de requisições.* O plano gratuito do Xano aceita 10 chamadas a
   cada 20 segundos. O tutor circula entre "meus pets", "marcar consulta" e
   "minhas consultas" olhando quase sempre os mesmos dados; com States
   separados, cada troca de página rebaixaria as mesmas tabelas. Aqui o que já
   veio fica, e `_garantir()` busca só o que falta.
2. *Vazamento.* O CRUD do Xano ainda devolve a tabela inteira — autorização por
   dono é a Fase 8. As listas cruas moram em vars com `_`, que o Reflex **não**
   envia ao navegador; para a tela vai só o recorte do tutor, montado aqui no
   servidor. Sem isso, os pets dos outros clientes chegariam ao browser dele:
   invisíveis na tela, visíveis no DevTools.

O filtro acontece no `load_*` e não num `@rx.var` porque as listas exibidas
precisam ser enriquecidas de qualquer jeito (nome do pet, nome do serviço, data
formatada) — é o mesmo desenho dos nove States do painel.
"""

import asyncio
from datetime import date, datetime, time, timedelta
from typing import Optional

import reflex as rx

from petbits import models, xano
from petbits.states.auth_state import AuthState
from petbits.states.conversores import (
    de_data_hora,
    formatar_data,
    formatar_data_hora,
    formatar_moeda,
    para_data,
    para_data_hora,
    para_input_data,
    para_numero,
)
from petbits.states.sessao import Sessao, SemSessao
from petbits.xano import SessaoExpirada, XanoError

# Expediente da clínica. O passo da agenda é a `duracao_estimada` do serviço
# escolhido; `PASSO_MINIMO` é o piso, para um serviço sem duração cadastrada
# não gerar um horário por minuto.
ABRE = 8
FECHA = 18
PASSO_MINIMO = 30

# Duas semanas cabem numa faixa horizontal sem virar calendário — e marcar com
# um mês de antecedência não é caso de uso de clínica de bairro.
DIAS_AGENDA = 14

DIAS_SEMANA = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]

# Status que ainda ocupam a agenda: um horário cancelado volta a ficar livre.
STATUS_OCUPAM = ("agendado", "em_andamento")

# As oito tabelas que o portal pode precisar, por apelido.
_FONTES = {
    "pets": "pets",
    "agendamentos": "agendamentos",
    "servicos": "servicos",
    "funcionarios": "funcionarios",
    "prontuarios": "prontuarios",
    "pedidos": "pedidos",
    "itens": "itens_pedido",
    "produtos": "produtos",
}


class PortalState(Sessao, rx.State):
    # --- dados crus: backend-only, nunca chegam ao navegador ---
    _pets: list[dict] = []
    _agendamentos: list[dict] = []
    _servicos: list[dict] = []
    _funcionarios: list[dict] = []
    _prontuarios: list[dict] = []
    _pedidos: list[dict] = []
    _itens: list[dict] = []
    _produtos: list[dict] = []
    _carregadas: list[str] = []

    cliente_id: int = 0
    cliente_nome: str = ""
    load_error: str = ""

    # --- meus pets ---
    pets: list[dict] = []
    pet_opcoes: list[dict] = []
    show_pet_dialog: bool = False
    pet_editing_id: Optional[int] = None
    pet_error: str = ""
    pet_nome: str = ""
    pet_especie: str = ""
    pet_raca: str = ""
    pet_data_nascimento: str = ""
    pet_peso: str = ""
    pet_observacoes: str = ""

    # --- minhas consultas ---
    consultas: list[dict] = []
    proxima_consulta: str = ""
    proxima_consulta_pet: str = ""

    # --- marcar consulta ---
    servico_opcoes: list[dict] = []
    dias: list[dict] = []
    horarios: list[dict] = []
    ag_pet: str = ""
    ag_servico: str = ""
    ag_dia: str = ""
    ag_hora: str = ""
    ag_observacoes: str = ""
    ag_error: str = ""
    ag_sucesso: str = ""
    ag_enviando: bool = False

    # --- histórico ---
    historico: list[dict] = []
    historico_pet: str = ""

    # --- minhas compras ---
    compras: list[dict] = []
    compra_aberta: Optional[int] = None
    compra_itens: list[dict] = []

    # ------------------------------------------------------------------
    # infraestrutura
    # ------------------------------------------------------------------

    async def _ficha(self, token: str):
        """Descobre qual cliente é o usuário logado. Uma vez por sessão."""
        if self.cliente_id:
            return
        ficha = await xano.minha_ficha(token)
        if ficha and ficha.get("id"):
            self.cliente_id = int(ficha["id"])
            self.cliente_nome = ficha.get("nome") or ""
            return
        # Sem ficha de tutor: ou é conta da equipe — que tem o painel, não o
        # portal — ou um cadastro que ficou pela metade.
        auth = await self.get_state(AuthState)
        raise SemSessao("/" if auth.eh_admin else "/sem-permissao")

    async def _garantir(self, *nomes: str, token: str, recarregar: bool = False):
        """Busca as tabelas pedidas, pulando as que já estão em memória."""
        faltando = [
            nome for nome in nomes
            if recarregar or nome not in self._carregadas
        ]
        if not faltando:
            return
        resultados = await asyncio.gather(
            *[
                getattr(models, _FONTES[nome]).listar(token=token)
                for nome in faltando
            ]
        )
        for nome, registros in zip(faltando, resultados):
            setattr(self, f"_{nome}", registros)
            if nome not in self._carregadas:
                self._carregadas.append(nome)

    def _meus_pets(self) -> list[dict]:
        return [p for p in self._pets if p.get("id_cliente") == self.cliente_id]

    def _meus_ids_pet(self) -> set:
        return {p["id"] for p in self._meus_pets() if p.get("id")}

    @staticmethod
    def _mapa(registros: list[dict], campo: str) -> dict:
        return {r["id"]: (r.get(campo) or "-") for r in registros if r.get("id")}

    # ------------------------------------------------------------------
    # /portal
    # ------------------------------------------------------------------

    async def load_inicio(self):
        self.load_error = ""
        try:
            token = await self._token(admin=False)
            await self._ficha(token)
            await self._garantir("pets", "agendamentos", "servicos", token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.load_error = str(erro)
            return

        self._montar_pets()
        self._montar_consultas()

    # ------------------------------------------------------------------
    # /portal/pets
    # ------------------------------------------------------------------

    @staticmethod
    def _idade(valor) -> str:
        """Idade em anos e meses — é o que o tutor reconhece, a data crua não."""
        momento = de_data_hora(valor)
        if not momento:
            return "-"
        hoje = date.today()
        nascimento = momento.date()
        meses = (hoje.year - nascimento.year) * 12 + hoje.month - nascimento.month
        if hoje.day < nascimento.day:
            meses -= 1
        if meses < 0:
            return "-"
        if meses < 12:
            return f"{meses} " + ("mês" if meses == 1 else "meses")
        anos, resto = divmod(meses, 12)
        texto = f"{anos} " + ("ano" if anos == 1 else "anos")
        return texto if resto == 0 else f"{texto} e {resto}m"

    def _montar_pets(self):
        self.pets = [
            {
                "id": p.get("id"),
                "nome": p.get("nome") or "-",
                "especie": p.get("especie") or "-",
                "raca": p.get("raca") or "-",
                "peso": formatar_moeda(p.get("peso")),
                "nascimento": formatar_data(p.get("data_nascimento")),
                "idade": self._idade(p.get("data_nascimento")),
                "observacoes": p.get("observacoes") or "",
            }
            for p in sorted(
                self._meus_pets(), key=lambda p: (p.get("nome") or "").lower()
            )
        ]
        self.pet_opcoes = [{"id": p["id"], "nome": p["nome"]} for p in self.pets]

    async def load_pets(self):
        self.load_error = ""
        try:
            token = await self._token(admin=False)
            await self._ficha(token)
            await self._garantir("pets", token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.pets = []
            self.load_error = str(erro)
            return
        self._montar_pets()

    def set_show_pet_dialog(self, value: bool):
        self.show_pet_dialog = value

    def set_pet_nome(self, value: str):
        self.pet_nome = value

    def set_pet_especie(self, value: str):
        self.pet_especie = value

    def set_pet_raca(self, value: str):
        self.pet_raca = value

    def set_pet_data_nascimento(self, value: str):
        self.pet_data_nascimento = value

    def set_pet_peso(self, value: str):
        self.pet_peso = value

    def set_pet_observacoes(self, value: str):
        self.pet_observacoes = value

    def novo_pet(self):
        self.pet_editing_id = None
        self.pet_error = ""
        self.pet_nome = ""
        self.pet_especie = ""
        self.pet_raca = ""
        self.pet_data_nascimento = ""
        self.pet_peso = ""
        self.pet_observacoes = ""
        self.show_pet_dialog = True

    def editar_pet(self, pet_id: int):
        bruto = next((p for p in self._pets if p.get("id") == pet_id), None)
        if bruto is None or bruto.get("id_cliente") != self.cliente_id:
            return
        self.pet_editing_id = pet_id
        self.pet_error = ""
        self.pet_nome = bruto.get("nome") or ""
        self.pet_especie = bruto.get("especie") or ""
        self.pet_raca = bruto.get("raca") or ""
        self.pet_data_nascimento = para_input_data(bruto.get("data_nascimento"))
        self.pet_peso = para_numero(bruto.get("peso"))
        self.pet_observacoes = bruto.get("observacoes") or ""
        self.show_pet_dialog = True

    def fechar_pet(self):
        self.show_pet_dialog = False
        self.pet_error = ""

    async def salvar_pet(self):
        if not self.pet_nome.strip():
            self.pet_error = "Informe o nome do pet."
            return
        if not self.pet_especie.strip():
            self.pet_error = "Informe a espécie."
            return
        peso = None
        if self.pet_peso.strip():
            try:
                peso = float(self.pet_peso.replace(",", "."))
            except ValueError:
                self.pet_error = "O peso precisa ser um número."
                return

        dados = {
            # O dono vem do servidor, nunca do formulário: é o que impede
            # cadastrar um pet na conta de outra pessoa.
            "id_cliente": self.cliente_id,
            "nome": self.pet_nome.strip(),
            "especie": self.pet_especie.strip(),
            "raca": self.pet_raca.strip(),
            "data_nascimento": para_data(self.pet_data_nascimento),
            "peso": peso,
            "observacoes": self.pet_observacoes.strip(),
        }

        try:
            token = await self._token(admin=False)
            if self.pet_editing_id is None:
                await models.pets.criar(dados, token=token)
            else:
                # A posse é conferida contra o registro carregado do banco,
                # nunca contra o que a tela mandou.
                atual = next(
                    (p for p in self._pets if p.get("id") == self.pet_editing_id),
                    None,
                )
                if atual is None or atual.get("id_cliente") != self.cliente_id:
                    self.pet_error = "Este pet não está na sua conta."
                    return
                await models.pets.atualizar(self.pet_editing_id, dados, token=token)
            await self._garantir("pets", token=token, recarregar=True)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.pet_error = str(erro)
            return

        self.show_pet_dialog = False
        self.pet_error = ""
        self._montar_pets()

    # ------------------------------------------------------------------
    # /portal/consultas
    # ------------------------------------------------------------------

    def _montar_consultas(self):
        meus = self._meus_ids_pet()
        nomes_pet = self._mapa(self._pets, "nome")
        nomes_servico = self._mapa(self._servicos, "nome_servico")
        agora = datetime.now()

        # A chave de ordenação é um `datetime` e fica fora do dicionário que
        # vai para a tela: tudo o que entra nas vars públicas é serializado e
        # mandado ao navegador, e ali só precisa do texto já formatado.
        linhas = []
        for a in self._agendamentos:
            if a.get("id_pet") not in meus:
                continue
            quando = de_data_hora(a.get("data_hora"))
            status = a.get("status") or "agendado"
            linhas.append(
                (
                    quando or datetime.min,
                    {
                        "id": a.get("id"),
                        "pet": nomes_pet.get(a.get("id_pet"), "-"),
                        "servico": nomes_servico.get(a.get("id_servico"), "-"),
                        "data_hora": formatar_data_hora(a.get("data_hora")),
                        "status": status,
                        "observacoes": a.get("observacoes") or "",
                        # Cancelar só faz sentido no que ainda vai acontecer.
                        "pode_cancelar": bool(
                            quando and quando > agora and status in STATUS_OCUPAM
                        ),
                    },
                )
            )
        linhas.sort(key=lambda par: par[0], reverse=True)
        self.consultas = [consulta for _, consulta in linhas]

        # A próxima consulta sai daqui e não do `load_inicio` porque este é o
        # único ponto que ainda tem os `datetime` na mão.
        futuras = [
            (quando, consulta)
            for quando, consulta in linhas
            if quando > agora and consulta["status"] in STATUS_OCUPAM
        ]
        if futuras:
            _, proxima = min(futuras, key=lambda par: par[0])
            self.proxima_consulta = f"{proxima['data_hora']} · {proxima['servico']}"
            self.proxima_consulta_pet = proxima["pet"]
        else:
            self.proxima_consulta = ""
            self.proxima_consulta_pet = ""

    async def load_consultas(self):
        self.load_error = ""
        try:
            token = await self._token(admin=False)
            await self._ficha(token)
            await self._garantir("pets", "agendamentos", "servicos", token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.consultas = []
            self.load_error = str(erro)
            return
        self._montar_consultas()

    async def cancelar_consulta(self, agendamento_id: int):
        self.load_error = ""
        try:
            token = await self._token(admin=False)
            atual = next(
                (a for a in self._agendamentos if a.get("id") == agendamento_id),
                None,
            )
            if atual is None or atual.get("id_pet") not in self._meus_ids_pet():
                self.load_error = "Esta consulta não está na sua conta."
                return
            await models.agendamentos.atualizar(
                agendamento_id, {**atual, "status": "cancelado"}, token=token
            )
            await self._garantir("agendamentos", token=token, recarregar=True)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        self._montar_consultas()

    # ------------------------------------------------------------------
    # /portal/agendar
    # ------------------------------------------------------------------

    async def load_agendar(self):
        self.load_error = ""
        self.ag_error = ""
        self.ag_sucesso = ""
        try:
            token = await self._token(admin=False)
            await self._ficha(token)
            await self._garantir(
                "pets", "agendamentos", "servicos", "funcionarios", token=token
            )
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.load_error = str(erro)
            return

        self._montar_pets()
        self.servico_opcoes = [
            {
                "id": s.get("id"),
                "nome": s.get("nome_servico") or "-",
                "preco": formatar_moeda(s.get("preco")),
                "duracao": max(
                    int(s.get("duracao_estimada") or PASSO_MINIMO), PASSO_MINIMO
                ),
            }
            for s in sorted(
                self._servicos, key=lambda s: (s.get("nome_servico") or "").lower()
            )
        ]
        if not self.ag_pet and self.pet_opcoes:
            self.ag_pet = str(self.pet_opcoes[0]["id"])
        if not self.ag_servico and self.servico_opcoes:
            self.ag_servico = str(self.servico_opcoes[0]["id"])
        self._montar_dias()
        self._montar_horarios()

    def set_ag_pet(self, value: str):
        self.ag_pet = value

    def set_ag_servico(self, value: str):
        # A duração do serviço é o passo da grade: trocar de serviço redesenha
        # os horários, e um horário que não existe mais não pode ficar marcado.
        self.ag_servico = value
        self.ag_hora = ""
        self._montar_horarios()

    def set_ag_dia(self, value: str):
        self.ag_dia = value
        self.ag_hora = ""
        self._montar_horarios()

    def set_ag_hora(self, value: str):
        self.ag_hora = value
        self.ag_error = ""

    def set_ag_observacoes(self, value: str):
        self.ag_observacoes = value

    def _montar_dias(self):
        hoje = date.today()
        self.dias = []
        for i in range(DIAS_AGENDA):
            dia = hoje + timedelta(days=i)
            # Domingo a clínica não abre; o dia simplesmente não aparece.
            if dia.weekday() == 6:
                continue
            self.dias.append(
                {
                    "valor": dia.isoformat(),
                    "semana": "Hoje" if i == 0 else DIAS_SEMANA[dia.weekday()],
                    "dia": str(dia.day),
                    "mes": MESES[dia.month - 1],
                }
            )
        if self.dias and self.ag_dia not in {d["valor"] for d in self.dias}:
            self.ag_dia = self.dias[0]["valor"]

    def _duracao_escolhida(self) -> int:
        escolhido = next(
            (s for s in self.servico_opcoes if str(s["id"]) == self.ag_servico), None
        )
        return int(escolhido["duracao"]) if escolhido else PASSO_MINIMO

    def _ocupacao(self) -> list:
        """Quem está ocupado, de quando a quando.

        A duração de cada compromisso vem do serviço **dele**, não do que está
        sendo marcado agora: um banho de 90 minutos não pode entrar na conta
        como 30 só porque a consulta nova dura 30.
        """
        duracoes = {
            s["id"]: max(int(s.get("duracao_estimada") or PASSO_MINIMO), PASSO_MINIMO)
            for s in self._servicos
            if s.get("id")
        }
        ocupados = []
        for a in self._agendamentos:
            if (a.get("status") or "agendado") not in STATUS_OCUPAM:
                continue
            inicio = de_data_hora(a.get("data_hora"))
            if not inicio:
                continue
            minutos = duracoes.get(a.get("id_servico"), PASSO_MINIMO)
            ocupados.append(
                (a.get("id_funcionario"), inicio, inicio + timedelta(minutes=minutos))
            )
        return ocupados

    def _quem_atende(self, inicio, fim, ocupacao, veterinarios):
        """O primeiro veterinário livre na faixa, ou None.

        O tutor não escolhe o profissional de propósito: a lista de quem
        trabalha na clínica, com CPF e telefone, não é informação de cliente —
        e para ele o que importa é o horário existir.
        """
        for vet in veterinarios:
            vet_id = vet.get("id")
            ocupado = any(
                f_id == vet_id and inicio < f_fim and f_inicio < fim
                for f_id, f_inicio, f_fim in ocupacao
            )
            if not ocupado:
                return vet_id
        return None

    def _montar_horarios(self):
        self.horarios = []
        if not self.ag_dia or not self.ag_servico:
            return
        try:
            dia = date.fromisoformat(self.ag_dia)
        except ValueError:
            return

        passo = self._duracao_escolhida()
        ocupacao = self._ocupacao()
        veterinarios = [
            f for f in self._funcionarios if f.get("cargo") == "veterinario"
        ]
        agora = datetime.now()
        momento = datetime.combine(dia, time(ABRE, 0))
        fecha = datetime.combine(dia, time(FECHA, 0))

        while momento + timedelta(minutes=passo) <= fecha:
            fim = momento + timedelta(minutes=passo)
            # Horário que já passou não aparece: mostrar desabilitado só
            # ocuparia a grade com o que ninguém pode escolher.
            if momento > agora:
                self.horarios.append(
                    {
                        "valor": momento.strftime("%H:%M"),
                        "livre": self._quem_atende(
                            momento, fim, ocupacao, veterinarios
                        )
                        is not None,
                    }
                )
            momento = fim

        if self.ag_hora not in {h["valor"] for h in self.horarios if h["livre"]}:
            self.ag_hora = ""

    @rx.var
    def tem_horario_livre(self) -> bool:
        return any(h["livre"] for h in self.horarios)

    async def agendar(self):
        self.ag_error = ""
        self.ag_sucesso = ""
        if not self.ag_pet:
            self.ag_error = "Escolha o pet."
            return
        if not self.ag_servico:
            self.ag_error = "Escolha o serviço."
            return
        if not self.ag_dia or not self.ag_hora:
            self.ag_error = "Escolha o dia e o horário."
            return

        try:
            pet_id = int(self.ag_pet)
            servico_id = int(self.ag_servico)
            inicio = datetime.fromisoformat(f"{self.ag_dia}T{self.ag_hora}")
        except ValueError:
            self.ag_error = "Horário inválido. Escolha de novo."
            return

        if pet_id not in self._meus_ids_pet():
            self.ag_error = "Este pet não está na sua conta."
            return

        self.ag_enviando = True
        yield

        try:
            token = await self._token(admin=False)
            # A agenda é relida antes de gravar: entre montar a tela e clicar
            # em confirmar, outra pessoa pode ter pegado o mesmo horário. Isto
            # estreita a janela, não a fecha — o CRUD do Xano não tem trava, e
            # fechá-la de verdade pede um endpoint dedicado.
            await self._garantir("agendamentos", token=token, recarregar=True)

            fim = inicio + timedelta(minutes=self._duracao_escolhida())
            veterinario = self._quem_atende(
                inicio,
                fim,
                self._ocupacao(),
                [f for f in self._funcionarios if f.get("cargo") == "veterinario"],
            )
            if veterinario is None:
                self.ag_enviando = False
                self.ag_error = (
                    "Esse horário acabou de ser preenchido. Escolha outro."
                )
                self._montar_horarios()
                return

            await models.agendamentos.criar(
                {
                    "id_pet": pet_id,
                    "id_servico": servico_id,
                    "id_funcionario": veterinario,
                    "data_hora": para_data_hora(f"{self.ag_dia}T{self.ag_hora}"),
                    "status": "agendado",
                    "observacoes": self.ag_observacoes.strip(),
                },
                token=token,
            )
            await self._garantir("agendamentos", token=token, recarregar=True)
        except (SemSessao, SessaoExpirada) as erro:
            self.ag_enviando = False
            yield await self._encerrar(erro)
            return
        except XanoError as erro:
            self.ag_enviando = False
            self.ag_error = str(erro)
            return

        nome_pet = next(
            (p["nome"] for p in self.pet_opcoes if str(p["id"]) == self.ag_pet), "seu pet"
        )
        self.ag_enviando = False
        self.ag_observacoes = ""
        self.ag_hora = ""
        self.ag_sucesso = (
            f"Consulta marcada para {nome_pet} em "
            f"{inicio.strftime('%d/%m/%Y às %H:%M')}."
        )
        self._montar_horarios()
        self._montar_consultas()

    # ------------------------------------------------------------------
    # /portal/historico
    # ------------------------------------------------------------------

    def set_historico_pet(self, value: str):
        self.historico_pet = value
        self._montar_historico()

    def _montar_historico(self):
        meus = self._meus_ids_pet()
        nomes_pet = self._mapa(self._pets, "nome")
        # Do funcionário sai só o nome: quem atendeu é informação do
        # atendimento, o resto da ficha dele não é.
        nomes_func = self._mapa(self._funcionarios, "nome")

        linhas = []
        for pr in self._prontuarios:
            id_pet = pr.get("id_pet")
            if id_pet not in meus:
                continue
            if self.historico_pet and str(id_pet) != self.historico_pet:
                continue
            linhas.append(
                (
                    de_data_hora(pr.get("data_atendimento")) or datetime.min,
                    {
                        "id": pr.get("id"),
                        "pet": nomes_pet.get(id_pet, "-"),
                        "profissional": nomes_func.get(pr.get("id_funcionario"), "-"),
                        "data": formatar_data_hora(pr.get("data_atendimento")),
                        "diagnostico": pr.get("diagnostico") or "-",
                        "tratamento": pr.get("tratamento_realizado") or "-",
                        "retorno": formatar_data(pr.get("proxima_consulta")),
                    },
                )
            )
        linhas.sort(key=lambda par: par[0], reverse=True)
        self.historico = [registro for _, registro in linhas]

    async def load_historico(self):
        self.load_error = ""
        try:
            token = await self._token(admin=False)
            await self._ficha(token)
            await self._garantir(
                "pets", "prontuarios", "funcionarios", token=token
            )
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.historico = []
            self.load_error = str(erro)
            return
        self._montar_pets()
        self._montar_historico()

    # ------------------------------------------------------------------
    # /portal/pedidos
    # ------------------------------------------------------------------

    def _montar_compras(self):
        linhas = []
        for p in self._pedidos:
            if p.get("id_cliente") != self.cliente_id:
                continue
            linhas.append(
                (
                    de_data_hora(p.get("data_pedido")) or datetime.min,
                    {
                        "id": p.get("id"),
                        "data": formatar_data_hora(p.get("data_pedido")),
                        "status": p.get("status") or "pendente",
                        "total": formatar_moeda(p.get("valor_total")),
                    },
                )
            )
        linhas.sort(key=lambda par: par[0], reverse=True)
        self.compras = [compra for _, compra in linhas]

    def abrir_compra(self, pedido_id: int):
        # Clicar de novo na mesma linha fecha — é o que se espera de uma linha
        # que expande.
        if self.compra_aberta == pedido_id:
            self.compra_aberta = None
            self.compra_itens = []
            return
        meus = {c["id"] for c in self.compras}
        if pedido_id not in meus:
            return
        nomes_produto = self._mapa(self._produtos, "nome")
        self.compra_aberta = pedido_id
        self.compra_itens = [
            {
                "id": i.get("id"),
                "produto": nomes_produto.get(i.get("id_produto"), "-"),
                "quantidade": i.get("quantidade") or 0,
                "unitario": formatar_moeda(i.get("valor_unitario")),
                "total": formatar_moeda(i.get("valor_total")),
            }
            for i in self._itens
            if i.get("id_pedido") == pedido_id
        ]

    async def load_compras(self):
        self.load_error = ""
        self.compra_aberta = None
        self.compra_itens = []
        try:
            token = await self._token(admin=False)
            await self._ficha(token)
            await self._garantir("pedidos", "itens", "produtos", token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.compras = []
            self.load_error = str(erro)
            return
        self._montar_compras()
