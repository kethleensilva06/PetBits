"""Página de cadastro de clientes (tutores)."""

import reflex as rx

from petbits.components import (
    data_table,
    error_banner,
    form_dialog,
    form_field,
    layout,
    page_toolbar,
    row_actions,
)
from petbits.states.cliente_state import ClienteState

COLUNAS = ["Nome", "CPF", "E-mail", "Telefone", "Endereço", "Ações"]


def _row(cliente: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(cliente["nome"]),
        rx.table.cell(cliente["cpf"]),
        rx.table.cell(cliente["email"]),
        rx.table.cell(cliente["telefone"]),
        rx.table.cell(cliente["endereco"]),
        rx.table.cell(
            row_actions(
                on_edit=ClienteState.open_edit(cliente),
                on_delete=ClienteState.delete(cliente["id"]),
                descricao_exclusao=(
                    "O tutor sai do cadastro e os pets dele ficam sem dono."
                ),
            )
        ),
    )


def _dialog() -> rx.Component:
    return form_dialog(
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
        aberto=ClienteState.show_dialog,
        on_open_change=ClienteState.set_show_dialog,
        titulo=rx.cond(ClienteState.editing_id, "Editar cliente", "Novo cliente"),
        erro=ClienteState.form_error,
        on_cancel=ClienteState.close_dialog,
        on_save=ClienteState.save,
        largura="30rem",
    )


def clientes_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ClienteState.search,
            on_search_change=ClienteState.set_search,
            on_new_click=ClienteState.open_new,
            new_label="Novo cliente",
        ),
        error_banner(ClienteState.load_error),
        data_table(
            COLUNAS,
            ClienteState.filtered_clientes,
            _row,
            vazio="Nenhum cliente cadastrado ainda.",
            busca=ClienteState.search,
        ),
        _dialog(),
        title="Clientes",
        subtitle="Tutores responsáveis pelos pets atendidos",
    )
