"""Página de agendamentos de serviços."""

import reflex as rx

from petbits.components import (
    empty_state,
    error_banner,
    form_field,
    layout,
    page_toolbar,
    row_actions,
)
from petbits.models import STATUS_AGENDAMENTO
from petbits.states.agendamento_state import AgendamentoState


def _row(agendamento: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(agendamento["data_hora"]),
        rx.table.cell(agendamento["pet_nome"]),
        rx.table.cell(agendamento["servico_nome"]),
        rx.table.cell(agendamento["funcionario_nome"]),
        rx.table.cell(
            rx.badge(
                agendamento["status"],
                color_scheme=rx.match(
                    agendamento["status"],
                    ("agendado", "blue"),
                    ("em_andamento", "amber"),
                    ("concluido", "green"),
                    ("cancelado", "red"),
                    "gray",
                ),
                variant="soft",
            )
        ),
        rx.table.cell(
            row_actions(
                on_edit=AgendamentoState.open_edit(agendamento),
                on_delete=AgendamentoState.delete(agendamento["id"]),
            )
        ),
    )


def _dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AgendamentoState.editing_id, "Editar agendamento", "Novo agendamento"
                )
            ),
            rx.vstack(
                form_field(
                    "Pet *",
                    rx.select.root(
                        rx.select.trigger(placeholder="Selecione o pet", width="100%"),
                        rx.select.content(
                            rx.foreach(
                                AgendamentoState.pet_options,
                                lambda p: rx.select.item(
                                    p["nome"], value=p["id"].to_string()
                                ),
                            )
                        ),
                        value=AgendamentoState.id_pet,
                        on_change=AgendamentoState.set_id_pet,
                        width="100%",
                    ),
                ),
                form_field(
                    "Serviço *",
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Selecione o serviço", width="100%"
                        ),
                        rx.select.content(
                            rx.foreach(
                                AgendamentoState.servico_options,
                                lambda s: rx.select.item(
                                    s["nome_servico"], value=s["id"].to_string()
                                ),
                            )
                        ),
                        value=AgendamentoState.id_servico,
                        on_change=AgendamentoState.set_id_servico,
                        width="100%",
                    ),
                ),
                form_field(
                    "Responsável *",
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Selecione o funcionário", width="100%"
                        ),
                        rx.select.content(
                            rx.foreach(
                                AgendamentoState.funcionario_options,
                                lambda f: rx.select.item(
                                    f["nome"], value=f["id"].to_string()
                                ),
                            )
                        ),
                        value=AgendamentoState.id_funcionario,
                        on_change=AgendamentoState.set_id_funcionario,
                        width="100%",
                    ),
                ),
                rx.hstack(
                    form_field(
                        "Data e hora *",
                        rx.input(
                            value=AgendamentoState.data_hora,
                            on_change=AgendamentoState.set_data_hora,
                            type="datetime-local",
                            width="100%",
                        ),
                    ),
                    form_field(
                        "Status",
                        rx.select(
                            STATUS_AGENDAMENTO,
                            value=AgendamentoState.status,
                            on_change=AgendamentoState.set_status,
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                form_field(
                    "Observações",
                    rx.text_area(
                        value=AgendamentoState.observacoes,
                        on_change=AgendamentoState.set_observacoes,
                        placeholder="Instruções para o atendimento",
                        width="100%",
                    ),
                ),
                rx.cond(
                    AgendamentoState.form_error,
                    rx.callout(
                        AgendamentoState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=AgendamentoState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=AgendamentoState.save),
                    justify="end",
                    spacing="3",
                    width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="34rem",
        ),
        open=AgendamentoState.show_dialog,
        on_open_change=AgendamentoState.set_show_dialog,
    )


def agendamentos_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=AgendamentoState.search,
            on_search_change=AgendamentoState.set_search,
            on_new_click=AgendamentoState.open_new,
            new_label="Novo agendamento",
        ),
        error_banner(AgendamentoState.load_error),
        rx.card(
            rx.cond(
                AgendamentoState.filtered_agendamentos,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Data/Hora"),
                            rx.table.column_header_cell("Pet"),
                            rx.table.column_header_cell("Serviço"),
                            rx.table.column_header_cell("Responsável"),
                            rx.table.column_header_cell("Status"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(AgendamentoState.filtered_agendamentos, _row)
                    ),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        AgendamentoState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum agendamento registrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _dialog(),
        title="Agendamentos",
        subtitle="Horários marcados para banho, tosa e consultas",
    )
