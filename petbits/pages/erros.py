"""Telas de porta fechada: sem permissão e página inexistente.

Ambas oferecem uma saída. Um beco sem saída num sistema com dois perfis é
especialmente ruim: o tutor que tropeça numa rota de admin precisa de um
caminho de volta ao portal, não de um texto dizendo que errou.
"""

import reflex as rx

from petbits.components.brand import logo
from petbits.states.auth_state import AuthState


def _tela(icone: str, cor: str, titulo: str, texto: str) -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.box(logo(size=30), padding_bottom="1.5rem"),
            rx.box(
                rx.icon(icone, size=34, color=rx.color(cor, 9)),
                padding="1rem",
                background=rx.color(cor, 3),
                border_radius="1rem",
                display="flex",
            ),
            rx.heading(titulo, size="7", font_family="Nunito, sans-serif"),
            rx.text(
                texto,
                size="3",
                color=rx.color("gray", 10),
                text_align="center",
                max_width="26rem",
            ),
            rx.hstack(
                rx.link(
                    rx.button(rx.icon("house", size=16), "Ir para o início", size="3"),
                    href=AuthState.rota_inicial,
                ),
                rx.cond(
                    AuthState.autenticado,
                    rx.button(
                        "Sair",
                        on_click=AuthState.sair,
                        size="3",
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.link(
                        rx.button(
                            "Entrar", size="3", variant="soft", color_scheme="gray"
                        ),
                        href="/login",
                    ),
                ),
                spacing="3",
                padding_top="0.5rem",
            ),
            spacing="4",
            align="center",
        ),
        min_height="100vh",
        padding="2rem",
        width="100%",
    )


def sem_permissao_page() -> rx.Component:
    return _tela(
        "lock",
        "amber",
        "Área restrita",
        "Esta parte do sistema é da equipe da clínica. Sua conta de tutor não "
        "tem acesso a ela.",
    )


def nao_encontrada_page() -> rx.Component:
    return _tela(
        "compass",
        "gray",
        "Página não encontrada",
        "O endereço que você abriu não existe — ou deixou de existir.",
    )
