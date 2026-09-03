"""Página de cadastro de serviços."""

import reflex as rx

from petbits.components import empty_state, form_field, layout, page_toolbar, row_actions
from petbits.states.servico_state import ServicoState


def _row(servico: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(servico["nome_servico"]),
        rx.table.cell(servico["descricao"]),
        rx.table.cell(f"R$ {servico['preco']}"),
        rx.table.cell(f"{servico['duracao_estimada']} min"),
        rx.table.cell(
            row_actions(
                on_edit=ServicoState.open_edit(servico),
                on_delete=ServicoState.delete(servico["id"]),
            )
        ),
    )


def _dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(ServicoState.editing_id, "Editar serviço", "Novo serviço")
            ),
            rx.vstack(
                form_field(
                    "Nome do serviço *",
                    rx.input(
                        value=ServicoState.nome_servico,
                        on_change=ServicoState.set_nome_servico,
                        placeholder="Banho e tosa",
                        width="100%",
                    ),
                ),
                form_field(
                    "Descrição",
                    rx.text_area(
                        value=ServicoState.descricao,
                        on_change=ServicoState.set_descricao,
                        placeholder="O que está incluído no serviço",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    form_field(
                        "Preço *",
                        rx.input(
                            value=ServicoState.preco,
                            on_change=ServicoState.set_preco,
                            type="number",
                            step="0.01",
                            width="100%",
                        ),
                    ),
                    form_field(
                        "Duração (min) *",
                        rx.input(
                            value=ServicoState.duracao_estimada,
                            on_change=ServicoState.set_duracao_estimada,
                            type="number",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.cond(
                    ServicoState.form_error,
                    rx.callout(
                        ServicoState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=ServicoState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=ServicoState.save),
                    justify="end",
                    spacing="3",
                    width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="32rem",
        ),
        open=ServicoState.show_dialog,
        on_open_change=ServicoState.set_show_dialog,
    )


def servicos_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ServicoState.search,
            on_search_change=ServicoState.set_search,
            on_new_click=ServicoState.open_new,
            new_label="Novo serviço",
        ),
        rx.card(
            rx.cond(
                ServicoState.filtered_servicos,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Serviço"),
                            rx.table.column_header_cell("Descrição"),
                            rx.table.column_header_cell("Preço"),
                            rx.table.column_header_cell("Duração"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(rx.foreach(ServicoState.filtered_servicos, _row)),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        ServicoState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum serviço cadastrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _dialog(),
        title="Serviços",
        subtitle="Procedimentos oferecidos pela clínica",
    )
