"""Pequenos componentes de UI reutilizados nas páginas de CRUD."""

import reflex as rx

from .tokens import STATUS_ROTULOS, de_mapa


def status_badge(valor, cores: dict[str, str]) -> rx.Component:
    """Badge de status, com o rótulo legível e a cor do mapa correspondente.

    `cores` é um dos mapas de `tokens.py` (agendamento ou pedido) — o rótulo
    sai sempre de `STATUS_ROTULOS`, que cobre os dois.
    """
    return rx.badge(
        de_mapa(valor, STATUS_ROTULOS, ""),
        color_scheme=de_mapa(valor, cores),
        variant="soft",
        radius="full",
    )


def money(valor) -> rx.Component:
    """Valor em reais, com dígitos de largura fixa para alinhar na coluna."""
    return rx.text(
        "R$ ", valor, size="2", font_variant_numeric="tabular-nums", as_="span"
    )


def stat_card(label: str, value, icon: str, href: str = "") -> rx.Component:
    """Cartão de indicador do painel. Vira link quando recebe `href`."""
    cartao = rx.card(
        rx.hstack(
            rx.box(
                rx.icon(icon, size=22, color=rx.color("accent", 9)),
                padding="0.6rem",
                background=rx.color("accent", 3),
                border_radius="0.6rem",
                display="flex",
            ),
            rx.vstack(
                rx.text(label, size="2", color=rx.color("gray", 10)),
                rx.heading(value, size="7"),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
    )
    if not href:
        return cartao
    return rx.link(cartao, href=href, underline="none", width="100%")


def section_card(titulo: str, *children, acao: rx.Component | None = None) -> rx.Component:
    """Cartão com cabeçalho e, opcionalmente, uma ação à direita do título."""
    cabecalho = rx.hstack(
        rx.heading(titulo, size="4"),
        rx.spacer(),
        acao if acao is not None else rx.fragment(),
        width="100%",
        align="center",
        padding_bottom="0.75rem",
    )
    return rx.card(
        rx.vstack(cabecalho, *children, spacing="0", width="100%"),
        width="100%",
    )


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


def error_banner(message) -> rx.Component:
    """Aviso exibido quando o Xano não responde ou recusa a requisição."""
    return rx.cond(
        message,
        rx.callout(
            message,
            icon="triangle_alert",
            color_scheme="red",
            width="100%",
        ),
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
