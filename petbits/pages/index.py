"""Página inicial: visão geral da clínica."""

import reflex as rx

from petbits.components import empty_state, layout
from petbits.states.dashboard_state import DashboardState


def _stat_card(label: str, value, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.card(
            rx.hstack(
                rx.box(
                    rx.icon(icon, size=22, color=rx.color("accent", 9)),
                    padding="0.6rem",
                    background=rx.color("accent", 3),
                    border_radius="0.6rem",
                ),
                rx.vstack(
                    rx.text(label, size="2", color=rx.color("gray", 10)),
                    rx.heading(value, size="6"),
                    spacing="0",
                    align_items="start",
                ),
                spacing="3",
                align="center",
            ),
            width="100%",
        ),
        href=href,
        underline="none",
        width="100%",
    )


def _agendamento_row(agendamento: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(agendamento["data_hora"]),
        rx.table.cell(agendamento["pet_nome"]),
        rx.table.cell(agendamento["servico_nome"]),
        rx.table.cell(agendamento["funcionario_nome"]),
        rx.table.cell(rx.badge(agendamento["status"], variant="soft")),
    )


def index() -> rx.Component:
    return layout(
        rx.grid(
            _stat_card("Clientes", DashboardState.total_clientes, "users", "/clientes"),
            _stat_card("Pets", DashboardState.total_pets, "paw-print", "/pets"),
            _stat_card(
                "Agendamentos hoje",
                DashboardState.agendamentos_hoje,
                "calendar-clock",
                "/agendamentos",
            ),
            _stat_card(
                "Pedidos pendentes",
                DashboardState.pedidos_pendentes,
                "shopping-cart",
                "/pedidos",
            ),
            _stat_card("Serviços", DashboardState.total_servicos, "stethoscope", "/servicos"),
            _stat_card("Produtos", DashboardState.total_produtos, "package", "/produtos"),
            _stat_card(
                "Funcionários",
                DashboardState.total_funcionarios,
                "id-card",
                "/funcionarios",
            ),
            columns="4",
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
