"""Página de prontuários (histórico clínico dos pets)."""

import reflex as rx

from petbits.components import (
    data_table,
    error_banner,
    form_dialog,
    form_field,
    layout,
    page_toolbar,
    row_actions,
    select_fk,
)
from petbits.states.prontuario_state import ProntuarioState

COLUNAS = [
    "Atendimento",
    "Pet",
    "Responsável",
    "Diagnóstico",
    "Próxima consulta",
    "Ações",
]


def _row(prontuario: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(prontuario["data_atendimento"]),
        rx.table.cell(prontuario["pet_nome"]),
        rx.table.cell(prontuario["funcionario_nome"]),
        rx.table.cell(prontuario["diagnostico"]),
        rx.table.cell(prontuario["proxima_consulta"]),
        rx.table.cell(
            row_actions(
                on_edit=ProntuarioState.open_edit(prontuario),
                on_delete=ProntuarioState.delete(prontuario["id"]),
                descricao_exclusao=(
                    "O atendimento sai do histórico clínico do pet, junto com "
                    "o diagnóstico e o tratamento registrados."
                ),
            )
        ),
    )


def _dialog() -> rx.Component:
    return form_dialog(
        select_fk(
            "Pet *",
            ProntuarioState.pet_options,
            "nome",
            ProntuarioState.id_pet,
            ProntuarioState.set_id_pet,
            placeholder="Selecione o pet",
        ),
        select_fk(
            "Responsável pelo atendimento *",
            ProntuarioState.funcionario_options,
            "nome",
            ProntuarioState.id_funcionario,
            ProntuarioState.set_id_funcionario,
            placeholder="Selecione o funcionário",
        ),
        form_field(
            "Diagnóstico",
            rx.text_area(
                value=ProntuarioState.diagnostico,
                on_change=ProntuarioState.set_diagnostico,
                placeholder="Quadro clínico observado",
                width="100%",
            ),
        ),
        form_field(
            "Tratamento realizado",
            rx.text_area(
                value=ProntuarioState.tratamento_realizado,
                on_change=ProntuarioState.set_tratamento_realizado,
                placeholder="Medicações, procedimentos, orientações",
                width="100%",
            ),
        ),
        form_field(
            "Próxima consulta",
            rx.input(
                value=ProntuarioState.proxima_consulta,
                on_change=ProntuarioState.set_proxima_consulta,
                type="date",
                width="100%",
            ),
        ),
        aberto=ProntuarioState.show_dialog,
        on_open_change=ProntuarioState.set_show_dialog,
        titulo=rx.cond(
            ProntuarioState.editing_id, "Editar prontuário", "Novo prontuário"
        ),
        erro=ProntuarioState.form_error,
        on_cancel=ProntuarioState.close_dialog,
        on_save=ProntuarioState.save,
        largura="36rem",
    )


def prontuarios_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ProntuarioState.search,
            on_search_change=ProntuarioState.set_search,
            on_new_click=ProntuarioState.open_new,
            new_label="Novo prontuário",
        ),
        error_banner(ProntuarioState.load_error),
        data_table(
            COLUNAS,
            ProntuarioState.filtered_prontuarios,
            _row,
            vazio="Nenhum prontuário registrado ainda.",
            busca=ProntuarioState.search,
        ),
        _dialog(),
        title="Prontuários",
        subtitle="Histórico clínico dos atendimentos realizados",
    )
