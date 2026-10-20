"""A agenda do tutor: marcar Clínica ou Banho e tosa num calendário.

A tela só oferece o que o backend aceitaria — dia de expediente, horário
livre, no futuro —, mas não é ela que garante: o `POST agendamentos` confere
tudo de novo (design.md da change `agendamento`, D2).
"""

import reflex as rx

from petbits import esqueletos
from petbits.agenda import DIAS_DA_SEMANA
from petbits.clinica import HORARIO_CURTO
from petbits.states.agenda_state import AgendaState
from petbits.visual import (LARGURA_DO_CLIENTE, campo, rodape_do_cliente, tela_vazia,
                            titulo_de_pagina, topo_do_cliente)


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
                    color=rx.color("gray", 11),
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
                            color=rx.color("gray", 11)),
                    rx.link("Cadastrar", href="/", size="2", weight="medium"),
                    spacing="2",
                ),
            ),
        ),
        spacing="5",
        width="100%",
    )


def _observacoes() -> rx.Component:
    return campo(
        "Observações para a clínica (opcional)",
        rx.text_area(
            placeholder="Ex.: ele fica nervoso com secador",
            value=AgendaState.observacoes,
            on_change=AgendaState.set_observacoes,
            width="100%",
        ),
    )


def _etapa(p: rx.Var) -> rx.Component:
    """Um passo da faixa de progresso (change `agenda-guiada`, D1)."""
    return rx.hstack(
        rx.center(
            rx.cond(p["feito"].to(bool), rx.icon("check", size=14), rx.text(p["numero"], size="1",
                                                                            weight="bold")),
            width="1.6rem",
            height="1.6rem",
            border_radius="9999px",
            flex_shrink="0",
            color=rx.cond(p["feito"].to(bool) | p["atual"].to(bool), "white",
                          rx.color("gray", 11)),
            background=rx.cond(p["feito"].to(bool), rx.color("teal", 9),
                               rx.cond(p["atual"].to(bool), rx.color("teal", 11),
                                       rx.color("gray", 4))),
        ),
        rx.text(p["rotulo"], size="2",
                weight=rx.cond(p["atual"].to(bool), "bold", "regular"),
                color=rx.cond(p["feito"].to(bool) | p["atual"].to(bool),
                              rx.color("gray", 12), rx.color("gray", 11))),
        spacing="2",
        align="center",
    )


def _progresso() -> rx.Component:
    return rx.grid(
        rx.foreach(AgendaState.passos, _etapa),
        columns=rx.breakpoints(initial="2", sm="4"),
        spacing="3",
        width="100%",
        padding="0.75rem 1rem",
        border_radius="1rem",
        background=rx.color("teal", 2),
        border=f"1px solid {rx.color('teal', 4)}",
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
                              color=rx.color("gray", 11)) for d in DIAS_DA_SEMANA],
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
                rx.text(HORARIO_CURTO,
                        size="1", color=rx.color("gray", 11)),
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
                    esqueletos.fichas("Buscando horários..."),
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
                                size="2", color=rx.color("gray", 11)),
                    ),
                ),
                spacing="2",
                width="100%",
                align_items="start",
            ),
        ),
    )


def _linha_do_resumo(l: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.text(l["rotulo"], size="2", color=rx.color("gray", 11), min_width="4.5rem"),
        rx.text(l["valor"], size="2",
                weight=rx.cond(l["escolhido"].to(bool), "medium", "regular"),
                color=rx.cond(l["escolhido"].to(bool), rx.color("gray", 12),
                              rx.color("gray", 11)),
                font_style=rx.cond(l["escolhido"].to(bool), "normal", "italic")),
        spacing="3",
        width="100%",
        align="start",
        padding_y="0.35rem",
        border_bottom=f"1px solid {rx.color('gray', 3)}",
    )


def _resumo() -> rx.Component:
    """O resumo fixo ao lado, com o Confirmar (change `agenda-guiada`, D2 e D3)."""
    return rx.card(
        rx.vstack(
            rx.hstack(rx.icon("clipboard-list", size=18, color=rx.color("teal", 10)),
                      rx.heading("Seu agendamento", size="4"), spacing="2", align="center"),
            rx.vstack(rx.foreach(AgendaState.linhas_do_resumo, _linha_do_resumo),
                      spacing="0", width="100%"),
            _observacoes(),
            rx.cond(
                AgendaState.erro,
                rx.callout(AgendaState.erro, icon="triangle_alert", color_scheme="red",
                           size="1", width="100%"),
            ),
            rx.button(
                rx.icon("calendar-check", size=16),
                "Confirmar agendamento",
                on_click=AgendaState.confirmar,
                disabled=AgendaState.enviando | (AgendaState.resumo == ""),
                loading=AgendaState.enviando,
                size="3",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
        position=rx.breakpoints(initial="static", md="sticky"),
        top="1rem",
    )


def _aviso_de_marcado() -> rx.Component:
    """O sucesso, com o compromisso para a agenda do celular (D4)."""
    return rx.cond(
        AgendaState.aviso,
        rx.callout.root(
            rx.callout.icon(rx.icon("circle_check")),
            rx.callout.text(AgendaState.aviso),
            rx.cond(
                AgendaState.ultimo_ics != "",
                rx.button(rx.icon("calendar-plus", size=14), "Adicionar à agenda do celular",
                          on_click=AgendaState.baixar_ics, variant="soft", color_scheme="green",
                          size="1", width="fit-content"),
            ),
            color_scheme="green",
            size="1",
            width="100%",
        ),
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
                        color=rx.color("gray", 11)),
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
                            size="1", color=rx.color("gray", 11), max_width="12rem"),
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
                AgendaState.mostrar_carregando,
                esqueletos.linhas("Carregando os seus agendamentos..."),
                # Falhou não é vazio: o erro já está no callout acima.
                rx.cond(AgendaState.erro_lista, rx.fragment(), tela_vazia(
                    "/fotos/vazio-agenda.webp",
                    "Nenhum agendamento ainda",
                    "Consulta, vacina ou banho e tosa: escolha o serviço, o animal e um "
                    "horário livre aqui em cima.",
                    rx.button(rx.icon("calendar-plus", size=16), "Marcar agora", size="3",
                              on_click=rx.scroll_to("marcar")),
                )),
            ),
        ),
        spacing="3",
        width="100%",
        align_items="start",
    )


def agenda_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            topo_do_cliente("/agenda"),
            titulo_de_pagina("Agendar", "Escolha o animal, o serviço e um horário livre."),
            _aviso_de_marcado(),
            _progresso(),
            # Passos numa coluna, resumo ao lado (change `agenda-guiada`, D3).
            rx.grid(
                rx.vstack(_escolhas(), _calendario(), spacing="5", width="100%"),
                _resumo(),
                columns=rx.breakpoints(initial="1", md="3fr 2fr"),
                spacing="6",
                width="100%",
                align_items="start",
                # Alvo do "Marcar agora" da tela vazia.
                id="marcar",
            ),
            rx.divider(margin_y="1rem"),
            _meus_agendamentos(),
            rodape_do_cliente(),
            spacing="4",
            align_items="start",
            padding_y="2rem",
            width="100%",
        ),
        size=LARGURA_DO_CLIENTE,
    )
