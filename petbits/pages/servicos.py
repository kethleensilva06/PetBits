"""Página de cadastro de serviços."""

import reflex as rx

from petbits.components import (
    data_table,
    error_banner,
    form_dialog,
    form_field,
    layout,
    money,
    page_toolbar,
    row_actions,
)
from petbits.states.servico_state import ServicoState

COLUNAS = ["Serviço", "Descrição", "Preço", "Duração", "Ações"]


def _row(servico: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(servico["nome_servico"]),
        rx.table.cell(servico["descricao"]),
        rx.table.cell(money(servico["preco"])),
        rx.table.cell(f"{servico['duracao_estimada']} min"),
        rx.table.cell(
            row_actions(
                on_edit=ServicoState.open_edit(servico),
                on_delete=ServicoState.delete(servico["id"]),
                descricao_exclusao=(
                    "O serviço sai do catálogo. Agendamentos que já o usam "
                    "continuam no histórico."
                ),
            )
        ),
    )


def _dialog() -> rx.Component:
    return form_dialog(
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
        aberto=ServicoState.show_dialog,
        on_open_change=ServicoState.set_show_dialog,
        titulo=rx.cond(ServicoState.editing_id, "Editar serviço", "Novo serviço"),
        erro=ServicoState.form_error,
        on_cancel=ServicoState.close_dialog,
        on_save=ServicoState.save,
    )


def servicos_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ServicoState.search,
            on_search_change=ServicoState.set_search,
            on_new_click=ServicoState.open_new,
            new_label="Novo serviço",
        ),
        error_banner(ServicoState.load_error),
        data_table(
            COLUNAS,
            ServicoState.filtered_servicos,
            _row,
            vazio="Nenhum serviço cadastrado ainda.",
            busca=ServicoState.search,
        ),
        _dialog(),
        title="Serviços",
        subtitle="Procedimentos oferecidos pela clínica",
    )
