"""A casa do tutor: os animais dele.

Deixou de ser um cartão de boas-vindas quando os animais passaram a existir.
O que aparece aqui é o que o backend devolveu — e o backend só devolve os
animais de quem perguntou.
"""

import reflex as rx

from petbits.states.auth_state import AuthState
from petbits.states.pet_state import PetState


def _campo(rotulo: str, componente: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(rotulo, size="2", weight="medium"),
        componente,
        spacing="1",
        width="100%",
        align_items="start",
    )


def _cartao(animal: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading(animal["nome"], size="4"),
                    rx.badge(animal["especie"], variant="soft", radius="full"),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(animal["raca"], size="2", color=rx.color("gray", 10)),
                rx.hstack(
                    rx.text("Nascimento: ", animal["nascimento"], size="1",
                            color=rx.color("gray", 10)),
                    rx.text("Peso: ", animal["peso"], " kg", size="1",
                            color=rx.color("gray", 10)),
                    spacing="4",
                    wrap="wrap",
                ),
                rx.cond(
                    animal["observacoes"],
                    rx.text(animal["observacoes"], size="1",
                            color=rx.color("gray", 11), padding_top="0.25rem"),
                ),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            rx.spacer(),
            rx.button(
                "Editar",
                on_click=lambda: PetState.editar(animal),
                variant="soft",
                size="1",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def _dialogo() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(PetState.titulo_dialogo),
            rx.vstack(
                _campo("Nome", rx.input(placeholder="Nome do animal",
                                        value=PetState.f_nome,
                                        on_change=PetState.set_f_nome,
                                        width="100%")),
                rx.hstack(
                    _campo("Espécie", rx.input(placeholder="Cão, gato...",
                                               value=PetState.f_especie,
                                               on_change=PetState.set_f_especie,
                                               width="100%")),
                    _campo("Raça", rx.input(placeholder="Opcional",
                                            value=PetState.f_raca,
                                            on_change=PetState.set_f_raca,
                                            width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                rx.hstack(
                    _campo("Nascimento", rx.input(type="date",
                                                  value=PetState.f_nascimento,
                                                  on_change=PetState.set_f_nascimento,
                                                  width="100%")),
                    _campo("Peso (kg)", rx.input(placeholder="Opcional",
                                                 value=PetState.f_peso,
                                                 on_change=PetState.set_f_peso,
                                                 width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                _campo("Observações", rx.text_area(
                    placeholder="Alergias, cuidados especiais...",
                    value=PetState.f_observacoes,
                    on_change=PetState.set_f_observacoes,
                    width="100%")),
                rx.cond(
                    PetState.form_error,
                    rx.callout(PetState.form_error, icon="triangle_alert",
                               color_scheme="red", size="1", width="100%"),
                ),
                rx.hstack(
                    rx.button("Cancelar", on_click=PetState.fechar,
                              variant="soft", color_scheme="gray"),
                    rx.button("Salvar", on_click=PetState.salvar,
                              disabled=PetState.salvando),
                    justify="end", spacing="3", width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="34rem",
        ),
        open=PetState.show_dialog,
        on_open_change=PetState.set_show_dialog,
    )


def _vazio() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Nenhum animal cadastrado ainda", size="4"),
            rx.text(
                "Cadastre o primeiro para a clínica poder acompanhá-lo.",
                size="2", color=rx.color("gray", 10),
            ),
            rx.button("Cadastrar animal", on_click=PetState.novo, size="3"),
            spacing="3", align="center", width="100%", padding="2.5rem",
        ),
        width="100%",
    )


def inicio_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("PetBits", size="6"),
                rx.spacer(),
                rx.badge(AuthState.papel_exibido, variant="soft", radius="full"),
                rx.button("Sair", on_click=AuthState.sair, variant="soft",
                          color_scheme="gray", size="2"),
                width="100%", align="center", padding_bottom="2rem",
            ),
            rx.hstack(
                rx.vstack(
                    rx.heading("Olá, ", AuthState.primeiro_nome, "!", size="7"),
                    rx.text("Os seus animais sob cuidado da clínica.",
                            color=rx.color("gray", 11)),
                    spacing="1", align_items="start",
                ),
                rx.spacer(),
                rx.cond(
                    PetState.tem_animais,
                    rx.button(rx.icon("plus", size=16), "Novo animal",
                              on_click=PetState.novo),
                    rx.fragment(),
                ),
                width="100%", align="center",
            ),
            rx.cond(
                PetState.load_error,
                rx.callout(PetState.load_error, icon="triangle_alert",
                           color_scheme="red", size="1", width="100%"),
            ),
            rx.cond(
                PetState.tem_animais,
                rx.grid(
                    rx.foreach(PetState.animais, _cartao),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="3", width="100%",
                ),
                _vazio(),
            ),
            _dialogo(),
            spacing="4", align_items="start", padding_y="3rem", width="100%",
        )
    )
