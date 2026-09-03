"""Página de cadastro de pets."""

import reflex as rx

from petbits.components import empty_state, form_field, layout, page_toolbar, row_actions
from petbits.states.pet_state import PetState


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
            )
        ),
    )


def _dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(rx.cond(PetState.editing_id, "Editar pet", "Novo pet")),
            rx.vstack(
                form_field(
                    "Tutor *",
                    rx.select.root(
                        rx.select.trigger(placeholder="Selecione o tutor", width="100%"),
                        rx.select.content(
                            rx.foreach(
                                PetState.cliente_options,
                                lambda c: rx.select.item(c.nome, value=c.id.to_string()),
                            )
                        ),
                        value=PetState.id_cliente,
                        on_change=PetState.set_id_cliente,
                        width="100%",
                    ),
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
                rx.cond(
                    PetState.form_error,
                    rx.callout(
                        PetState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=PetState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=PetState.save),
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
        open=PetState.show_dialog,
        on_open_change=PetState.set_show_dialog,
    )


def pets_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=PetState.search,
            on_search_change=PetState.set_search,
            on_new_click=PetState.open_new,
            new_label="Novo pet",
        ),
        rx.card(
            rx.cond(
                PetState.filtered_pets,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Nome"),
                            rx.table.column_header_cell("Espécie"),
                            rx.table.column_header_cell("Raça"),
                            rx.table.column_header_cell("Peso"),
                            rx.table.column_header_cell("Tutor"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(rx.foreach(PetState.filtered_pets, _row)),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        PetState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum pet cadastrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _dialog(),
        title="Pets",
        subtitle="Animais atendidos pela clínica",
    )
