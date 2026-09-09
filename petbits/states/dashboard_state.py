"""Estado da página inicial: indicadores e próximos agendamentos."""

import asyncio
from datetime import datetime

import reflex as rx

from petbits import models
from petbits.states.conversores import de_data_hora, formatar_data_hora
from petbits.xano import XanoError


class DashboardState(rx.State):
    total_clientes: int = 0
    total_pets: int = 0
    total_funcionarios: int = 0
    total_produtos: int = 0
    total_servicos: int = 0
    agendamentos_hoje: int = 0
    pedidos_pendentes: int = 0
    proximos_agendamentos: list[dict] = []
    load_error: str = ""

    async def load_dashboard(self):
        self.load_error = ""
        try:
            (
                clientes,
                pets,
                funcionarios,
                produtos,
                servicos,
                pedidos,
                agendamentos,
            ) = await asyncio.gather(
                models.clientes.listar(),
                models.pets.listar(),
                models.funcionarios.listar(),
                models.produtos.listar(),
                models.servicos.listar(),
                models.pedidos.listar(),
                models.agendamentos.listar(),
            )
        except XanoError as erro:
            self.total_clientes = 0
            self.total_pets = 0
            self.total_funcionarios = 0
            self.total_produtos = 0
            self.total_servicos = 0
            self.agendamentos_hoje = 0
            self.pedidos_pendentes = 0
            self.proximos_agendamentos = []
            self.load_error = str(erro)
            return

        pets_por_id = {p.get("id"): p.get("nome") for p in pets}
        servicos_por_id = {s.get("id"): s.get("nome_servico") for s in servicos}
        funcionarios_por_id = {f.get("id"): f.get("nome") for f in funcionarios}

        hoje = datetime.now().date()
        agora = datetime.now()

        # A data e hora de cada agendamento é convertida uma única vez.
        marcados = [(de_data_hora(a.get("data_hora")), a) for a in agendamentos]

        self.total_clientes = len(clientes)
        self.total_pets = len(pets)
        self.total_funcionarios = len(funcionarios)
        self.total_produtos = len(produtos)
        self.total_servicos = len(servicos)
        self.agendamentos_hoje = len(
            [a for momento, a in marcados if momento and momento.date() == hoje]
        )
        self.pedidos_pendentes = len(
            [p for p in pedidos if p.get("status") == "pendente"]
        )

        futuros = sorted(
            (
                a
                for momento, a in marcados
                if momento
                and momento >= agora
                and a.get("status") in ("agendado", "em_andamento")
            ),
            key=lambda a: a.get("data_hora") or 0,
        )

        self.proximos_agendamentos = [
            {
                "id": a.get("id"),
                "pet_nome": pets_por_id.get(a.get("id_pet")) or "Pet removido",
                "servico_nome": (
                    servicos_por_id.get(a.get("id_servico")) or "Serviço removido"
                ),
                "funcionario_nome": (
                    funcionarios_por_id.get(a.get("id_funcionario"))
                    or "Funcionário removido"
                ),
                "data_hora": formatar_data_hora(a.get("data_hora")),
                "status": a.get("status") or "-",
            }
            for a in futuros[:8]
        ]
