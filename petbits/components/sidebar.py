"""Menu lateral de navegação entre as páginas do PetBits."""

import reflex as rx

from .brand import logo

NAV_ITEMS = [
    ("Início", "/", "layout-dashboard"),
    ("Clientes", "/clientes", "users"),
    ("Pets", "/pets", "paw-print"),
    ("Agendamentos", "/agendamentos", "calendar-clock"),
    ("Prontuários", "/prontuarios", "clipboard-list"),
    ("Serviços", "/servicos", "stethoscope"),
    ("Produtos", "/produtos", "package"),
    ("Pedidos", "/pedidos", "shopping-cart"),
    ("Funcionários", "/funcionarios", "id-card"),
]


def _nav_link(label: str, href: str, icon: str) -> rx.Component:
    is_active = rx.State.router.page.path == href
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(label, size="3"),
            spacing="3",
            align="center",
        ),
        href=href,
        width="100%",
        padding="0.5rem 0.75rem",
        border_radius="0.5rem",
        background=rx.cond(is_active, rx.color("accent", 4), "transparent"),
        color=rx.cond(is_active, rx.color("accent", 11), rx.color("gray", 11)),
        _hover={"background": rx.color("accent", 3)},
        weight=rx.cond(is_active, "bold", "regular"),
        underline="none",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(logo(size=30), padding_bottom="1rem"),
            *[_nav_link(label, href, icon) for label, href, icon in NAV_ITEMS],
            rx.spacer(),
            rx.hstack(
                rx.color_mode.button(),
                rx.text("Clínica Veterinária", size="1", color=rx.color("gray", 9)),
                align="center",
                spacing="2",
                padding_top="1rem",
            ),
            height="100%",
            width="100%",
            align_items="stretch",
        ),
        width="15rem",
        min_width="15rem",
        height="100vh",
        padding="1.25rem 1rem",
        border_right=f"1px solid {rx.color('gray', 5)}",
        position="sticky",
        top="0",
    )
