"""Página de cadastro de pets."""

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
from petbits.states.pet_state import PetState

COLUNAS = ["Nome", "Espécie", "Raça", "Peso", "Tutor", "Ações"]


def _row(pet: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(pet["nome"]),
        rx.table.cell(pet["especie"]),
        rx.table.cell(pet["raca"]),
        rx.table.cell(rx.cond(pet["peso"], f"{pet['peso']} kg", "-")),
        rx.table.cell(pet["cliente_nome"]),
        rx.table.cell(
            row_actions(
                on_edit=PetState.open_edit(pet),
                on_delete=PetState.delete(pet["id"]),
                descricao_exclusao=(
                    "O pet sai da ficha do tutor. Agendamentos já registrados "
                    "continuam no histórico."
                ),
            )
        ),
    )


def _dialog() -> rx.Component:
    return form_dialog(
        select_fk(
            "Tutor *",
            PetState.cliente_options,
            "nome",
            PetState.id_cliente,
            PetState.set_id_cliente,
            placeholder="Selecione o tutor",
        ),
        form_field(
            "Nome *",
            rx.input(
                value=PetState.nome,
                on_change=PetState.set_nome,
                placeholder="Nome do pet",
                width="100%",
            ),
        ),
        rx.hstack(
            form_field(
                "Espécie *",
                rx.input(
                    value=PetState.especie,
                    on_change=PetState.set_especie,
                    placeholder="Cão, gato...",
                    width="100%",
                ),
            ),
            form_field(
                "Raça",
                rx.input(
                    value=PetState.raca,
                    on_change=PetState.set_raca,
                    placeholder="SRD, Poodle...",
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        rx.hstack(
            form_field(
                "Data de nascimento",
                rx.input(
                    value=PetState.data_nascimento,
                    on_change=PetState.set_data_nascimento,
                    type="date",
                    width="100%",
                ),
            ),
            form_field(
                "Peso (kg)",
                rx.input(
                    value=PetState.peso,
                    on_change=PetState.set_peso,
                    placeholder="0.0",
                    type="number",
                    step="0.1",
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        form_field(
            "Observações",
            rx.text_area(
                value=PetState.observacoes,
                on_change=PetState.set_observacoes,
                placeholder="Alergias, comportamento, cuidados especiais...",
                width="100%",
            ),
        ),
        aberto=PetState.show_dialog,
        on_open_change=PetState.set_show_dialog,
        titulo=rx.cond(PetState.editing_id, "Editar pet", "Novo pet"),
        erro=PetState.form_error,
        on_cancel=PetState.close_dialog,
        on_save=PetState.save,
        largura="34rem",
    )


def pets_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=PetState.search,
            on_search_change=PetState.set_search,
            on_new_click=PetState.open_new,
            new_label="Novo pet",
        ),
        error_banner(PetState.load_error),
        data_table(
            COLUNAS,
            PetState.filtered_pets,
            _row,
            vazio="Nenhum pet cadastrado ainda.",
            busca=PetState.search,
        ),
        _dialog(),
        title="Pets",
        subtitle="Animais atendidos pela clínica",
    )
