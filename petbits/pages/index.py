"""Página inicial: visão geral da clínica."""

import reflex as rx

from petbits.components import (
    STATUS_AGENDAMENTO_CORES,
    empty_state,
    error_banner,
    layout,
    stat_card,
    status_badge,
)
from petbits.states.dashboard_state import DashboardState


def _agendamento_row(agendamento: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(agendamento["data_hora"]),
        rx.table.cell(agendamento["pet_nome"]),
        rx.table.cell(agendamento["servico_nome"]),
        rx.table.cell(agendamento["funcionario_nome"]),
        rx.table.cell(
            status_badge(agendamento["status"], STATUS_AGENDAMENTO_CORES)
        ),
    )


def index() -> rx.Component:
    return layout(
        error_banner(DashboardState.load_error),
        rx.grid(
            stat_card("Clientes", DashboardState.total_clientes, "users", "/clientes"),
            stat_card("Pets", DashboardState.total_pets, "paw-print", "/pets"),
            stat_card(
                "Agendamentos hoje",
                DashboardState.agendamentos_hoje,
                "calendar-clock",
                "/agendamentos",
            ),
            stat_card(
                "Pedidos pendentes",
                DashboardState.pedidos_pendentes,
                "shopping-cart",
                "/pedidos",
            ),
            stat_card("Serviços", DashboardState.total_servicos, "stethoscope", "/servicos"),
            stat_card("Produtos", DashboardState.total_produtos, "package", "/produtos"),
            stat_card(
                "Funcionários",
                DashboardState.total_funcionarios,
                "id-card",
                "/funcionarios",
            ),
            columns=rx.breakpoints(initial="1", sm="2", lg="4"),
            spacing="4",
            width="100%",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Próximos agendamentos", size="4"),
                rx.cond(
                    DashboardState.proximos_agendamentos,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Data/Hora"),
                                rx.table.column_header_cell("Pet"),
                                rx.table.column_header_cell("Serviço"),
                                rx.table.column_header_cell("Responsável"),
                                rx.table.column_header_cell("Status"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                DashboardState.proximos_agendamentos, _agendamento_row
                            )
                        ),
                        width="100%",
                    ),
                    empty_state("Nenhum agendamento futuro registrado."),
                ),
                spacing="3",
                width="100%",
                align_items="start",
            ),
            width="100%",
        ),
        title="Painel PetBits",
        subtitle="Visão geral da clínica veterinária",
    )
