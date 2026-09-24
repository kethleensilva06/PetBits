"""Página de cadastro de funcionários."""

import reflex as rx

from petbits import models
from petbits.components import (
    data_table,
    error_banner,
    form_dialog,
    form_field,
    layout,
    page_toolbar,
    row_actions,
)
from petbits.states.funcionario_state import FuncionarioState

COLUNAS = ["Nome", "CPF", "Cargo", "Telefone", "E-mail", "Ações"]


def _row(funcionario: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(funcionario["nome"]),
        rx.table.cell(funcionario["cpf"]),
        rx.table.cell(rx.badge(funcionario["cargo"], variant="soft")),
        rx.table.cell(funcionario["telefone"]),
        rx.table.cell(funcionario["email"]),
        rx.table.cell(
            row_actions(
                on_edit=FuncionarioState.open_edit(funcionario),
                on_delete=FuncionarioState.delete(funcionario["id"]),
                descricao_exclusao=(
                    "O funcionário sai da equipe. Agendamentos já atendidos "
                    "por ele continuam no histórico."
                ),
            )
        ),
    )


def _dialog() -> rx.Component:
    return form_dialog(
        form_field(
            "Nome *",
            rx.input(
                value=FuncionarioState.nome,
                on_change=FuncionarioState.set_nome,
                placeholder="Nome completo",
                width="100%",
            ),
        ),
        rx.hstack(
            form_field(
                "CPF *",
                rx.input(
                    value=FuncionarioState.cpf,
                    on_change=FuncionarioState.set_cpf,
                    placeholder="000.000.000-00",
                    max_length=14,
                    width="100%",
                ),
            ),
            form_field(
                "Cargo *",
                rx.select(
                    models.CARGOS_FUNCIONARIO,
                    value=FuncionarioState.cargo,
                    on_change=FuncionarioState.set_cargo,
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        rx.hstack(
            form_field(
                "Telefone",
                rx.input(
                    value=FuncionarioState.telefone,
                    on_change=FuncionarioState.set_telefone,
                    placeholder="(00) 00000-0000",
                    width="100%",
                ),
            ),
            form_field(
                "E-mail",
                rx.input(
                    value=FuncionarioState.email,
                    on_change=FuncionarioState.set_email,
                    placeholder="funcionario@petbits.com",
                    type="email",
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        form_field(
            "Data de contratação",
            rx.input(
                value=FuncionarioState.data_contratacao,
                on_change=FuncionarioState.set_data_contratacao,
                type="date",
                width="100%",
            ),
        ),
        aberto=FuncionarioState.show_dialog,
        on_open_change=FuncionarioState.set_show_dialog,
        titulo=rx.cond(
            FuncionarioState.editing_id, "Editar funcionário", "Novo funcionário"
        ),
        erro=FuncionarioState.form_error,
        on_cancel=FuncionarioState.close_dialog,
        on_save=FuncionarioState.save,
        largura="34rem",
    )


def funcionarios_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=FuncionarioState.search,
            on_search_change=FuncionarioState.set_search,
            on_new_click=FuncionarioState.open_new,
            new_label="Novo funcionário",
        ),
        error_banner(FuncionarioState.load_error),
        data_table(
            COLUNAS,
            FuncionarioState.filtered_funcionarios,
            _row,
            vazio="Nenhum funcionário cadastrado ainda.",
            busca=FuncionarioState.search,
        ),
        _dialog(),
        title="Funcionários",
        subtitle="Equipe da clínica: veterinários, tosadores e atendentes",
    )
