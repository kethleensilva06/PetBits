"""Layouts das páginas do PetBits.

Dois cascos com a mesma estrutura e menus diferentes: `layout()` para as telas
da clínica e `layout_cliente()` para o portal do tutor. A assinatura de
`layout()` não mudou, então as nove páginas existentes seguem intactas.
"""

import reflex as rx

from .sidebar import NAV_ADMIN, NAV_CLIENTE, sidebar


def _casca(itens, children, title: str, subtitle: str) -> rx.Component:
    header = rx.vstack(
        rx.heading(title, size="7"),
        rx.text(subtitle, color=rx.color("gray", 10)) if subtitle else rx.fragment(),
        spacing="1",
        padding_bottom="1.5rem",
        align_items="start",
        width="100%",
    ) if title else rx.fragment()

    return rx.hstack(
        sidebar(itens),
        rx.box(
            header,
            rx.vstack(*children, spacing="4", width="100%", align_items="stretch"),
            padding="2rem 2.5rem",
            width="100%",
            max_width="80rem",
            margin="0 auto",
        ),
        align_items="start",
        width="100%",
        spacing="0",
    )


def layout(*children, title: str = "", subtitle: str = "") -> rx.Component:
    """Telas da equipe da clínica."""
    return _casca(NAV_ADMIN, children, title, subtitle)


def layout_cliente(*children, title: str = "", subtitle: str = "") -> rx.Component:
    """Telas do portal do tutor."""
    return _casca(NAV_CLIENTE, children, title, subtitle)
