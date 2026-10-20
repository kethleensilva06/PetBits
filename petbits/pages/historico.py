"""O histórico clínico na tela (change `historico-clinico`, D5).

A linha do tempo é a mesma nas duas áreas; na clínica cada atendimento tem
"Retificar", e o diálogo tem "Registrar atendimento". Não há botão de editar
nem de apagar em lugar nenhum: o histórico não se apaga.
"""

import reflex as rx

from petbits.states.historico_state import HistoricoEquipeState, HistoricoTutorState


def _linha(rotulo: str, valor) -> rx.Component:
    return rx.cond(valor, rx.text(rx.text.strong(rotulo, ": "), valor, size="2"))


def _atendimento(item, *, com_retificar: bool) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("stethoscope", size=16, color=rx.color("teal", 10)),
                rx.text(item["data"], weight="bold"),
                rx.text(item["quem"], size="2", color=rx.color("gray", 11)),
                rx.cond(item["retificado"],
                        rx.badge("Retificado", color_scheme="amber", variant="soft",
                                 radius="full")),
                rx.cond(item["e_retificacao"],
                        rx.badge("Retificação de ", item["retifica_data"], color_scheme="teal",
                                 variant="soft", radius="full")),
                rx.spacer(),
                rx.button("Retificar", on_click=HistoricoEquipeState.retificar(item),
                          variant="soft", color_scheme="gray", size="1")
                if com_retificar else rx.fragment(),
                spacing="2", align="center", wrap="wrap", width="100%",
            ),
            _linha("Motivo", item["motivo"]),
            rx.text(rx.text.strong("Diagnóstico: "), item["diagnostico"], size="2"),
            _linha("Tratamento", item["tratamento"]),
            rx.hstack(
                rx.cond(item["peso"], rx.badge("Peso: ", item["peso"], variant="surface",
                                               color_scheme="gray", radius="full")),
                rx.cond(item["retorno"], rx.badge(rx.icon("calendar", size=12), "Retorno: ",
                                                  item["retorno"], variant="soft",
                                                  color_scheme="orange", radius="full")),
                spacing="2", wrap="wrap",
            ),
            spacing="1", align_items="start", width="100%",
            # O retificado continua visível, só mais apagado: a correção é a
            # que vale, mas o que foi escrito antes não some.
            opacity=rx.cond(item["retificado"], "0.6", "1"),
        ),
        width="100%",
    )


def _linha_do_tempo(S, *, com_retificar: bool, vazio: str) -> rx.Component:
    return rx.cond(
        S.carregando,
        rx.hstack(rx.spinner(size="2"), rx.text("Carregando o histórico..."), spacing="2"),
        rx.cond(
            S.erro,
            rx.callout(S.erro, icon="triangle_alert", color_scheme="red", size="1", width="100%"),
            rx.cond(
                S.itens.length() > 0,
                rx.vstack(rx.foreach(S.itens, lambda i: _atendimento(i, com_retificar=com_retificar)),
                          spacing="2", width="100%"),
                rx.vstack(
                    rx.icon("clipboard-list", size=28, color=rx.color("gray", 9)),
                    rx.text(vazio, size="2", color=rx.color("gray", 11), text_align="center"),
                    spacing="2", align="center", width="100%", padding="1.5rem",
                ),
            ),
        ),
    )


def dialogo_historico_equipe() -> rx.Component:
    S = HistoricoEquipeState
    return rx.dialog.root(
        rx.dialog.content(
            rx.hstack(
                rx.dialog.title("Histórico de ", S.pet_nome, margin="0"),
                rx.spacer(),
                rx.button(rx.icon("plus", size=16), "Registrar atendimento", on_click=S.novo,
                          size="2"),
                align="center", width="100%", wrap="wrap", spacing="3",
            ),
            rx.text("Do mais recente ao mais antigo. Um atendimento não se apaga: para "
                    "corrigir, retifique.", size="1", color=rx.color("gray", 10),
                    margin_bottom="0.75rem"),
            rx.scroll_area(
                _linha_do_tempo(S, com_retificar=True,
                                vazio="Ainda não há atendimento registrado para este animal."),
                max_height="60vh", type="auto", scrollbars="vertical",
            ),
            max_width="44rem",
        ),
        open=S.aberto,
        on_open_change=S.set_aberto,
    )


def _campo(rotulo: str, componente: rx.Component) -> rx.Component:
    return rx.vstack(rx.text(rotulo, size="2", weight="medium"), componente,
                     spacing="1", width="100%", align_items="start")


def dialogo_form_atendimento() -> rx.Component:
    S = HistoricoEquipeState
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(S.titulo_form, " · ", S.pet_nome),
            rx.cond(S.f_retifica,
                    rx.callout(rx.text.span("Isto registra uma retificação do atendimento de ",
                                            S.f_retifica_data, ". O original continua no "
                                            "histórico, marcado como retificado."),
                               icon="info", size="1", width="100%", margin_bottom="0.5rem")),
            rx.cond(S.f_agendamento,
                    rx.callout("Registrar conclui o agendamento.", icon="circle_check",
                               size="1", width="100%", margin_bottom="0.5rem")),
            rx.vstack(
                rx.grid(
                    _campo("Quem atendeu", rx.select.root(
                        rx.select.trigger(placeholder="Veterinário ou clínico geral",
                                          width="100%"),
                        rx.select.content(rx.foreach(
                            S.profissionais,
                            lambda p: rx.select.item(p["rotulo"], value=p["id"]))),
                        value=S.f_colaborador, on_change=S.set_f_colaborador)),
                    _campo("Data", rx.input(type="date", value=S.f_data,
                                            on_change=S.set_f_data, width="100%")),
                    columns=rx.breakpoints(initial="1", sm="2"), spacing="3", width="100%",
                ),
                _campo("Motivo", rx.input(placeholder="Consulta de rotina, vacina, queixa...",
                                          value=S.f_motivo, on_change=S.set_f_motivo,
                                          width="100%")),
                _campo("Diagnóstico", rx.text_area(value=S.f_diagnostico,
                                                   on_change=S.set_f_diagnostico,
                                                   width="100%")),
                _campo("Tratamento realizado", rx.text_area(
                    placeholder="Opcional", value=S.f_tratamento,
                    on_change=S.set_f_tratamento, width="100%")),
                rx.grid(
                    _campo("Peso no dia (kg)", rx.input(placeholder="Opcional",
                                                        value=S.f_peso,
                                                        on_change=S.set_f_peso,
                                                        width="100%")),
                    _campo("Retorno", rx.input(type="date", value=S.f_retorno,
                                               on_change=S.set_f_retorno, width="100%")),
                    columns=rx.breakpoints(initial="1", sm="2"), spacing="3", width="100%",
                ),
                rx.cond(S.form_erro, rx.callout(S.form_erro, icon="triangle_alert",
                                                color_scheme="red", size="1", width="100%")),
                rx.hstack(
                    rx.button("Cancelar", on_click=S.set_form_aberto(False), variant="soft",
                              color_scheme="gray"),
                    rx.button("Registrar", on_click=S.salvar, disabled=S.salvando),
                    justify="end", spacing="3", width="100%", padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="38rem",
        ),
        open=S.form_aberto,
        on_open_change=S.set_form_aberto,
    )


def dialogo_historico_tutor() -> rx.Component:
    S = HistoricoTutorState
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Histórico de ", S.pet_nome),
            rx.text("Os atendimentos registrados pela clínica, do mais recente ao mais antigo.",
                    size="1", color=rx.color("gray", 10), margin_bottom="0.75rem"),
            rx.scroll_area(
                _linha_do_tempo(S, com_retificar=False,
                                vazio="Ainda não há atendimento registrado. Depois da "
                                      "primeira consulta, ele aparece aqui."),
                max_height="60vh", type="auto", scrollbars="vertical",
            ),
            rx.dialog.close(rx.button("Fechar", variant="soft", color_scheme="gray",
                                      margin_top="0.75rem")),
            max_width="40rem",
        ),
        open=S.aberto,
        on_open_change=S.set_aberto,
    )
