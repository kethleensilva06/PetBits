"""Layout base compartilhado por todas as páginas do PetBits."""

import reflex as rx

from .sidebar import sidebar


def layout(*children, title: str = "", subtitle: str = "") -> rx.Component:
    header = rx.vstack(
        rx.heading(title, size="7"),
        rx.text(subtitle, color=rx.color("gray", 10)) if subtitle else rx.fragment(),
        spacing="1",
        padding_bottom="1.5rem",
        align_items="start",
        width="100%",
    ) if title else rx.fragment()

    return rx.hstack(
        sidebar(),
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
