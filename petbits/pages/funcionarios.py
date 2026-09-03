"""Página de cadastro de funcionários."""

import reflex as rx

from petbits.components import empty_state, form_field, layout, page_toolbar, row_actions
from petbits.models import CARGOS_FUNCIONARIO, Funcionario
from petbits.states.funcionario_state import FuncionarioState


def _row(funcionario: Funcionario) -> rx.Component:
    return rx.table.row(
        rx.table.cell(funcionario.nome),
        rx.table.cell(funcionario.cpf),
        rx.table.cell(rx.badge(funcionario.cargo, variant="soft")),
        rx.table.cell(rx.cond(funcionario.telefone, funcionario.telefone, "-")),
        rx.table.cell(rx.cond(funcionario.email, funcionario.email, "-")),
        rx.table.cell(
            row_actions(
                on_edit=FuncionarioState.open_edit(funcionario),
                on_delete=FuncionarioState.delete(funcionario.id),
            )
        ),
    )


def _dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    FuncionarioState.editing_id, "Editar funcionário", "Novo funcionário"
                )
            ),
            rx.vstack(
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
                            CARGOS_FUNCIONARIO,
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
                rx.cond(
                    FuncionarioState.form_error,
                    rx.callout(
                        FuncionarioState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=FuncionarioState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=FuncionarioState.save),
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
        open=FuncionarioState.show_dialog,
        on_open_change=FuncionarioState.set_show_dialog,
    )


def funcionarios_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=FuncionarioState.search,
            on_search_change=FuncionarioState.set_search,
            on_new_click=FuncionarioState.open_new,
            new_label="Novo funcionário",
        ),
        rx.card(
            rx.cond(
                FuncionarioState.filtered_funcionarios,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Nome"),
                            rx.table.column_header_cell("CPF"),
                            rx.table.column_header_cell("Cargo"),
                            rx.table.column_header_cell("Telefone"),
                            rx.table.column_header_cell("E-mail"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(FuncionarioState.filtered_funcionarios, _row)
                    ),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        FuncionarioState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum funcionário cadastrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _dialog(),
        title="Funcionários",
        subtitle="Equipe da clínica: veterinários, tosadores e atendentes",
    )
