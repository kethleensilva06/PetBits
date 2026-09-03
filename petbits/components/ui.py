"""Pequenos componentes de UI reutilizados nas páginas de CRUD."""

import reflex as rx


def form_field(label: str, input_component: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color=rx.color("gray", 11)),
        input_component,
        spacing="1",
        width="100%",
        align_items="start",
    )


def row_actions(on_edit, on_delete) -> rx.Component:
    return rx.hstack(
        rx.icon_button(
            rx.icon("pencil", size=16),
            on_click=on_edit,
            variant="soft",
            size="1",
        ),
        rx.icon_button(
            rx.icon("trash-2", size=16),
            on_click=on_delete,
            variant="soft",
            color_scheme="red",
            size="1",
        ),
        spacing="2",
    )


def empty_state(message) -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon("inbox", size=32, color=rx.color("gray", 8)),
            rx.text(message, color=rx.color("gray", 9)),
            spacing="2",
        ),
        padding="3rem",
        width="100%",
    )


def page_toolbar(search_value, on_search_change, on_new_click, new_label: str) -> rx.Component:
    return rx.hstack(
        rx.input(
            rx.input.slot(rx.icon("search", size=16)),
            placeholder="Buscar...",
            value=search_value,
            on_change=on_search_change,
            width="20rem",
        ),
        rx.spacer(),
        rx.button(
            rx.icon("plus", size=16),
            new_label,
            on_click=on_new_click,
        ),
        width="100%",
        align="center",
    )
