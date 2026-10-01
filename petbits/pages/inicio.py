"""A tela pós-login.

Mínima de propósito: esta change entrega a porta de entrada, não o sistema.
O conteúdo chega nas changes seguintes — meus animais, agenda, histórico.
O que ela já prova é que a sessão existe, sabe quem é a pessoa e sobrevive a
recarregar a página.
"""

import reflex as rx

from petbits.states.auth_state import AuthState


def inicio_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("PetBits", size="6"),
                rx.spacer(),
                rx.badge(AuthState.papel_exibido, variant="soft", radius="full"),
                rx.button(
                    "Sair",
                    on_click=AuthState.sair,
                    variant="soft",
                    color_scheme="gray",
                    size="2",
                ),
                width="100%",
                align="center",
                padding_bottom="2rem",
            ),
            rx.heading("Olá, ", AuthState.primeiro_nome, "!", size="8"),
            rx.text(
                "Sua conta está criada e você está autenticado.",
                color=rx.color("gray", 11),
            ),
            rx.cond(
                AuthState.erro,
                rx.callout(
                    AuthState.erro,
                    icon="triangle_alert",
                    color_scheme="amber",
                    size="1",
                    width="100%",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.text("O que vem a seguir", size="2", weight="bold"),
                    rx.text(
                        "Cada funcionalidade entra por uma change do OpenSpec: "
                        "cadastrar os seus animais, marcar atendimento, "
                        "acompanhar o histórico clínico e as compras.",
                        size="2",
                        color=rx.color("gray", 10),
                    ),
                    spacing="2",
                    align_items="start",
                ),
                width="100%",
                margin_top="1rem",
            ),
            spacing="3",
            align_items="start",
            padding_y="3rem",
        )
    )
