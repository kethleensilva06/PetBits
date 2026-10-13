"""A agenda do tutor: marcar Clínica ou Banho e tosa num calendário.

A tela só oferece o que o backend aceitaria — dia de expediente, horário
livre, no futuro —, mas não é ela que garante: o `POST agendamentos` confere
tudo de novo (design.md da change `agendamento`, D2).
"""

import reflex as rx

from petbits.agenda import DIAS_DA_SEMANA
from petbits.states.agenda_state import AgendaState
from petbits.states.auth_state import AuthState


def _passo(numero: str, titulo: str, *conteudo) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.badge(numero, radius="full", variant="solid", size="2"),
            rx.text(titulo, size="3", weight="bold"),
            spacing="2",
            align="center",
        ),
        *conteudo,
        spacing="2",
        width="100%",
        align_items="start",
    )


def _escolhas() -> rx.Component:
    return rx.vstack(
        _passo(
            "1",
            "O que você quer marcar?",
            rx.segmented_control.root(
                rx.segmented_control.item("Clínica", value="clinica"),
                rx.segmented_control.item("Banho e tosa", value="banho_tosa"),
                value=AgendaState.categoria,
                on_change=AgendaState.set_categoria,
                width="100%",
            ),
            rx.cond(
                AgendaState.servicos_da_categoria.length() > 0,
                rx.select.root(
                    rx.select.trigger(placeholder="Escolha o serviço", width="100%"),
                    rx.select.content(
                        rx.foreach(
                            AgendaState.servicos_da_categoria,
                            lambda s: rx.select.item(
                                s["nome"], " · ", s["duracao"], " min · ", s["preco"],
                                value=s["id"].to_string(),
                            ),
                        ),
                    ),
                    value=AgendaState.servico_id,
                    on_change=AgendaState.set_servico_id,
                    width="100%",
                ),
                rx.text(
                    "A clínica ainda não disponibilizou serviços nesta categoria.",
                    size="2",
                    color=rx.color("gray", 10),
                ),
            ),
        ),
        _passo(
            "2",
            "Para qual animal?",
            rx.cond(
                AgendaState.animais.length() > 0,
                rx.select.root(
                    rx.select.trigger(placeholder="Escolha o animal", width="100%"),
                    rx.select.content(
                        rx.foreach(
                            AgendaState.animais,
                            lambda a: rx.select.item(a["nome"], value=a["id"].to_string()),
                        ),
                    ),
                    value=AgendaState.pet_id,
                    on_change=AgendaState.set_pet_id,
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Você ainda não cadastrou nenhum animal.", size="2",
                            color=rx.color("gray", 10)),
                    rx.link("Cadastrar", href="/", size="2", weight="medium"),
                    spacing="2",
                ),
            ),
        ),
        spacing="5",
        width="100%",
    )


def _observacoes() -> rx.Component:
    return _passo(
        "4",
        "Observações para a clínica (opcional)",
        rx.text_area(
            placeholder="Ex.: ele fica nervoso com secador",
            value=AgendaState.observacoes,
            on_change=AgendaState.set_observacoes,
            width="100%",
        ),
    )


def _dia(dia: rx.Var) -> rx.Component:
    return rx.cond(
        dia["numero"] == "",
        rx.box(),
        rx.button(
            dia["numero"],
            on_click=AgendaState.escolher_dia(dia["iso"]),
            disabled=~dia["habilitado"].to(bool),
            variant=rx.cond(dia["escolhido"].to(bool), "solid", "soft"),
            color_scheme=rx.cond(dia["habilitado"].to(bool), "teal", "gray"),
            width="100%",
            height="2.5rem",
        ),
    )


def _calendario() -> rx.Component:
    return _passo(
        "3",
        "Escolha o dia e o horário",
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon_button(rx.icon("chevron_left"), on_click=AgendaState.mes_anterior,
                                   disabled=~AgendaState.pode_voltar_mes, variant="ghost",
                                   aria_label="Mês anterior"),
                    rx.spacer(),
                    rx.text(AgendaState.titulo_do_mes, weight="bold"),
                    rx.spacer(),
                    rx.icon_button(rx.icon("chevron_right"), on_click=AgendaState.mes_seguinte,
                                   variant="ghost", aria_label="Próximo mês"),
                    width="100%",
                    align="center",
                ),
                rx.grid(
                    *[rx.text(d, size="1", weight="medium", align="center",
                              color=rx.color("gray", 10)) for d in DIAS_DA_SEMANA],
                    columns="7",
                    spacing="1",
                    width="100%",
                ),
                rx.foreach(
                    AgendaState.semanas,
                    lambda semana: rx.grid(
                        rx.foreach(semana, _dia),
                        columns="7",
                        spacing="1",
                        width="100%",
                    ),
                ),
                rx.text("Domingo fechado · seg a sex 8h–18h · sábado 8h–12h",
                        size="1", color=rx.color("gray", 9)),
                spacing="2",
                width="100%",
            ),
            width="100%",
        ),
        rx.cond(
            AgendaState.dia_iso != "",
            rx.vstack(
                rx.text(AgendaState.dia_por_extenso, size="2", weight="medium"),
                rx.cond(
                    AgendaState.buscando_horarios,
                    rx.hstack(rx.spinner(size="1"),
                              rx.text("Buscando horários...", size="2"), spacing="2"),
                    rx.cond(
                        AgendaState.horarios.length() > 0,
                        rx.flex(
                            rx.foreach(
                                AgendaState.horarios,
                                lambda h: rx.button(
                                    h["rotulo"],
                                    on_click=AgendaState.escolher_horario(h["ms"]),
                                    variant=rx.cond(AgendaState.horario_ms == h["ms"],
                                                    "solid", "outline"),
                                    size="2",
                                ),
                            ),
                            wrap="wrap",
                            gap="2",
                        ),
                        rx.text("Nenhum horário livre neste dia. Tente outro.",
                                size="2", color=rx.color("gray", 10)),
                    ),
                ),
                spacing="2",
                width="100%",
                align_items="start",
            ),
        ),
    )


def _confirmacao() -> rx.Component:
    return rx.vstack(
        rx.cond(
            AgendaState.resumo != "",
            rx.callout(AgendaState.resumo, icon="calendar_check", size="1", width="100%"),
        ),
        rx.cond(
            AgendaState.erro,
            rx.callout(AgendaState.erro, icon="triangle_alert", color_scheme="red",
                       size="1", width="100%"),
        ),
        rx.button(
            "Confirmar agendamento",
            on_click=AgendaState.confirmar,
            disabled=AgendaState.enviando | (AgendaState.resumo == ""),
            size="3",
            width="100%",
        ),
        spacing="3",
        width="100%",
    )


def _item(a: rx.Var) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text(a["servico"], weight="bold"),
                    rx.badge(a["categoria"], variant="soft", radius="full"),
                    rx.badge(a["situacao"], radius="full",
                             color_scheme=rx.cond(a["cancelado"].to(bool), "gray", "teal")),
                    spacing="2",
                    wrap="wrap",
                    align="center",
                ),
                rx.text(a["quando"], size="2"),
                rx.text(a["animal"], " · ", a["profissional"], size="1",
                        color=rx.color("gray", 10)),
                spacing="1",
                align_items="start",
            ),
            rx.spacer(),
            rx.cond(
                a["pode_cancelar"].to(bool),
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Cancelar", variant="soft", color_scheme="red", size="1"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Cancelar agendamento?"),
                        rx.alert_dialog.description(
                            a["servico"], " · ", a["quando"],
                        ),
                        rx.hstack(
                            rx.alert_dialog.cancel(rx.button("Voltar", variant="soft",
                                                             color_scheme="gray")),
                            rx.alert_dialog.action(rx.button(
                                "Cancelar agendamento", color_scheme="red",
                                on_click=AgendaState.cancelar(a["id"]),
                            )),
                            spacing="3",
                            justify="end",
                            padding_top="1rem",
                        ),
                    ),
                ),
                rx.cond(
                    a["dentro_do_prazo"].to(bool),
                    rx.text("Menos de 24 h: para cancelar, fale com a clínica.",
                            size="1", color=rx.color("gray", 10), max_width="12rem"),
                ),
            ),
            align="start",
            width="100%",
        ),
        width="100%",
    )


def _meus_agendamentos() -> rx.Component:
    return rx.vstack(
        rx.heading("Meus agendamentos", size="5"),
        rx.cond(
            AgendaState.erro_lista,
            rx.callout(AgendaState.erro_lista, icon="triangle_alert", color_scheme="red",
                       size="1", width="100%"),
        ),
        rx.cond(
            AgendaState.tem_agendamentos,
            rx.vstack(rx.foreach(AgendaState.agendamentos, _item), spacing="2", width="100%"),
            rx.cond(
                AgendaState.carregando,
                rx.hstack(rx.spinner(size="1"), rx.text("Carregando...", size="2"), spacing="2"),
                rx.text("Nenhum agendamento ainda.", size="2", color=rx.color("gray", 10)),
            ),
        ),
        spacing="3",
        width="100%",
        align_items="start",
    )


def agenda_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.link(rx.heading("PetBits", size="6"), href="/", underline="none",
                        color="inherit"),
                rx.spacer(),
                rx.link("Meus animais", href="/", size="2"),
                rx.button("Sair", on_click=AuthState.sair, variant="soft",
                          color_scheme="gray", size="2"),
                width="100%",
                align="center",
                spacing="4",
                padding_bottom="1.5rem",
            ),
            rx.heading("Agendar", size="7"),
            rx.cond(
                AgendaState.aviso,
                rx.callout(AgendaState.aviso, icon="circle_check", color_scheme="green",
                           size="1", width="100%"),
            ),
            rx.grid(
                rx.vstack(_escolhas(), spacing="4", width="100%"),
                rx.vstack(_calendario(), _observacoes(), _confirmacao(), spacing="4",
                          width="100%"),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="6",
                width="100%",
            ),
            rx.divider(margin_y="1rem"),
            _meus_agendamentos(),
            spacing="4",
            align_items="start",
            padding_y="3rem",
            width="100%",
        ),
    )
