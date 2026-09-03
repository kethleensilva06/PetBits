"""Página de cadastro de clientes (tutores)."""

import reflex as rx

from petbits.components import empty_state, form_field, layout, page_toolbar, row_actions
from petbits.models import Cliente
from petbits.states.cliente_state import ClienteState


def _row(cliente: Cliente) -> rx.Component:
    return rx.table.row(
        rx.table.cell(cliente.nome),
        rx.table.cell(cliente.cpf),
        rx.table.cell(rx.cond(cliente.email, cliente.email, "-")),
        rx.table.cell(rx.cond(cliente.telefone, cliente.telefone, "-")),
        rx.table.cell(rx.cond(cliente.endereco, cliente.endereco, "-")),
        rx.table.cell(
            row_actions(
                on_edit=ClienteState.open_edit(cliente),
                on_delete=ClienteState.delete(cliente.id),
            )
        ),
    )


def _dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(ClienteState.editing_id, "Editar cliente", "Novo cliente")
            ),
            rx.vstack(
                form_field(
                    "Nome *",
                    rx.input(
                        value=ClienteState.nome,
                        on_change=ClienteState.set_nome,
                        placeholder="Nome completo",
                        width="100%",
                    ),
                ),
                form_field(
                    "CPF *",
                    rx.input(
                        value=ClienteState.cpf,
                        on_change=ClienteState.set_cpf,
                        placeholder="000.000.000-00",
                        max_length=14,
                        width="100%",
                    ),
                ),
                form_field(
                    "E-mail",
                    rx.input(
                        value=ClienteState.email,
                        on_change=ClienteState.set_email,
                        placeholder="cliente@email.com",
                        type="email",
                        width="100%",
                    ),
                ),
                form_field(
                    "Telefone",
                    rx.input(
                        value=ClienteState.telefone,
                        on_change=ClienteState.set_telefone,
                        placeholder="(00) 00000-0000",
                        width="100%",
                    ),
                ),
                form_field(
                    "Endereço",
                    rx.input(
                        value=ClienteState.endereco,
                        on_change=ClienteState.set_endereco,
                        placeholder="Rua, número, bairro, cidade",
                        width="100%",
                    ),
                ),
                rx.cond(
                    ClienteState.form_error,
                    rx.callout(
                        ClienteState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=ClienteState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=ClienteState.save),
                    justify="end",
                    spacing="3",
                    width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="30rem",
        ),
        open=ClienteState.show_dialog,
        on_open_change=ClienteState.set_show_dialog,
    )


def clientes_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ClienteState.search,
            on_search_change=ClienteState.set_search,
            on_new_click=ClienteState.open_new,
            new_label="Novo cliente",
        ),
        rx.card(
            rx.cond(
                ClienteState.filtered_clientes,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Nome"),
                            rx.table.column_header_cell("CPF"),
                            rx.table.column_header_cell("E-mail"),
                            rx.table.column_header_cell("Telefone"),
                            rx.table.column_header_cell("Endereço"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(rx.foreach(ClienteState.filtered_clientes, _row)),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        ClienteState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum cliente cadastrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _dialog(),
        title="Clientes",
        subtitle="Tutores responsáveis pelos pets atendidos",
    )
