"""Página de prontuários (histórico clínico dos pets)."""

import reflex as rx

from petbits.components import empty_state, form_field, layout, page_toolbar, row_actions
from petbits.states.prontuario_state import ProntuarioState


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
            )
        ),
    )


def _dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    ProntuarioState.editing_id, "Editar prontuário", "Novo prontuário"
                )
            ),
            rx.vstack(
                form_field(
                    "Pet *",
                    rx.select.root(
                        rx.select.trigger(placeholder="Selecione o pet", width="100%"),
                        rx.select.content(
                            rx.foreach(
                                ProntuarioState.pet_options,
                                lambda p: rx.select.item(p.nome, value=p.id.to_string()),
                            )
                        ),
                        value=ProntuarioState.id_pet,
                        on_change=ProntuarioState.set_id_pet,
                        width="100%",
                    ),
                ),
                form_field(
                    "Responsável pelo atendimento *",
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Selecione o funcionário", width="100%"
                        ),
                        rx.select.content(
                            rx.foreach(
                                ProntuarioState.funcionario_options,
                                lambda f: rx.select.item(f.nome, value=f.id.to_string()),
                            )
                        ),
                        value=ProntuarioState.id_funcionario,
                        on_change=ProntuarioState.set_id_funcionario,
                        width="100%",
                    ),
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
                rx.cond(
                    ProntuarioState.form_error,
                    rx.callout(
                        ProntuarioState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=ProntuarioState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=ProntuarioState.save),
                    justify="end",
                    spacing="3",
                    width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="36rem",
        ),
        open=ProntuarioState.show_dialog,
        on_open_change=ProntuarioState.set_show_dialog,
    )


def prontuarios_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ProntuarioState.search,
            on_search_change=ProntuarioState.set_search,
            on_new_click=ProntuarioState.open_new,
            new_label="Novo prontuário",
        ),
        rx.card(
            rx.cond(
                ProntuarioState.filtered_prontuarios,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Atendimento"),
                            rx.table.column_header_cell("Pet"),
                            rx.table.column_header_cell("Responsável"),
                            rx.table.column_header_cell("Diagnóstico"),
                            rx.table.column_header_cell("Próxima consulta"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(ProntuarioState.filtered_prontuarios, _row)
                    ),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        ProntuarioState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum prontuário registrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _dialog(),
        title="Prontuários",
        subtitle="Histórico clínico dos atendimentos realizados",
    )
