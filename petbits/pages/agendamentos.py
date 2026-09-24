"""Página de agendamentos de serviços."""

import reflex as rx

from petbits.components import (
    STATUS_AGENDAMENTO_CORES,
    data_table,
    error_banner,
    form_dialog,
    form_field,
    layout,
    page_toolbar,
    row_actions,
    select_fk,
    status_badge,
)
from petbits.models import STATUS_AGENDAMENTO
from petbits.states.agendamento_state import AgendamentoState

COLUNAS = ["Data/Hora", "Pet", "Serviço", "Responsável", "Status", "Ações"]


def _row(agendamento: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(agendamento["data_hora"]),
        rx.table.cell(agendamento["pet_nome"]),
        rx.table.cell(agendamento["servico_nome"]),
        rx.table.cell(agendamento["funcionario_nome"]),
        rx.table.cell(
            status_badge(agendamento["status"], STATUS_AGENDAMENTO_CORES)
        ),
        rx.table.cell(
            row_actions(
                on_edit=AgendamentoState.open_edit(agendamento),
                on_delete=AgendamentoState.delete(agendamento["id"]),
                descricao_exclusao=(
                    "O horário volta a ficar livre na agenda e o registro do "
                    "atendimento se perde."
                ),
            )
        ),
    )


def _dialog() -> rx.Component:
    return form_dialog(
        select_fk(
            "Pet *",
            AgendamentoState.pet_options,
            "nome",
            AgendamentoState.id_pet,
            AgendamentoState.set_id_pet,
            placeholder="Selecione o pet",
        ),
        select_fk(
            "Serviço *",
            AgendamentoState.servico_options,
            "nome_servico",
            AgendamentoState.id_servico,
            AgendamentoState.set_id_servico,
            placeholder="Selecione o serviço",
        ),
        select_fk(
            "Responsável *",
            AgendamentoState.funcionario_options,
            "nome",
            AgendamentoState.id_funcionario,
            AgendamentoState.set_id_funcionario,
            placeholder="Selecione o funcionário",
        ),
        rx.hstack(
            form_field(
                "Data e hora *",
                rx.input(
                    value=AgendamentoState.data_hora,
                    on_change=AgendamentoState.set_data_hora,
                    type="datetime-local",
                    width="100%",
                ),
            ),
            form_field(
                "Status",
                rx.select(
                    STATUS_AGENDAMENTO,
                    value=AgendamentoState.status,
                    on_change=AgendamentoState.set_status,
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        form_field(
            "Observações",
            rx.text_area(
                value=AgendamentoState.observacoes,
                on_change=AgendamentoState.set_observacoes,
                placeholder="Instruções para o atendimento",
                width="100%",
            ),
        ),
        aberto=AgendamentoState.show_dialog,
        on_open_change=AgendamentoState.set_show_dialog,
        titulo=rx.cond(
            AgendamentoState.editing_id, "Editar agendamento", "Novo agendamento"
        ),
        erro=AgendamentoState.form_error,
        on_cancel=AgendamentoState.close_dialog,
        on_save=AgendamentoState.save,
        largura="34rem",
    )


def agendamentos_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=AgendamentoState.search,
            on_search_change=AgendamentoState.set_search,
            on_new_click=AgendamentoState.open_new,
            new_label="Novo agendamento",
        ),
        error_banner(AgendamentoState.load_error),
        data_table(
            COLUNAS,
            AgendamentoState.filtered_agendamentos,
            _row,
            vazio="Nenhum agendamento registrado ainda.",
            busca=AgendamentoState.search,
        ),
        _dialog(),
        title="Agendamentos",
        subtitle="Horários marcados para banho, tosa e consultas",
    )
