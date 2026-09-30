"""Menu lateral de navegação.

Há dois menus, não um menu com itens escondidos: a equipe da clínica e o tutor
usam o sistema para coisas diferentes, e uma lista de nove itens com seis
apagados só ensinaria ao tutor o que ele não pode fazer. Esconder item é
conforto, não segurança — quem barra de verdade é o Xano.
"""

import reflex as rx

from petbits.states.auth_state import AuthState

from .brand import logo

NAV_ADMIN = [
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

NAV_CLIENTE = [
    ("Início", "/portal", "house"),
    ("Meus pets", "/portal/pets", "paw-print"),
    ("Marcar consulta", "/portal/agendar", "calendar-plus"),
    ("Minhas consultas", "/portal/consultas", "calendar-clock"),
    ("Histórico", "/portal/historico", "clipboard-list"),
    ("Minhas compras", "/portal/pedidos", "shopping-bag"),
]


def _nav_link(label: str, href: str, icon: str) -> rx.Component:
    is_active = rx.State.router.url.path == href
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


def user_menu() -> rx.Component:
    """Rodapé da barra: quem está logado, e a saída.

    O papel aparece por escrito porque o mesmo sistema tem duas caras — sem
    isso, um admin que testa a conta de tutor perde a noção de onde está.
    """
    return rx.menu.root(
        rx.menu.trigger(
            rx.hstack(
                rx.avatar(
                    fallback=AuthState.iniciais,
                    size="2",
                    radius="full",
                    color_scheme="jade",
                ),
                rx.vstack(
                    rx.text(
                        AuthState.primeiro_nome,
                        size="2",
                        weight="medium",
                        trim="both",
                    ),
                    rx.text(
                        rx.cond(AuthState.eh_admin, "Equipe", "Tutor"),
                        size="1",
                        color=rx.color("gray", 10),
                        trim="both",
                    ),
                    spacing="0",
                    align_items="start",
                ),
                rx.spacer(),
                rx.icon("chevrons-up-down", size=14, color=rx.color("gray", 9)),
                width="100%",
                align="center",
                spacing="2",
                padding="0.5rem",
                border_radius="0.5rem",
                cursor="pointer",
                _hover={"background": rx.color("gray", 3)},
            )
        ),
        rx.menu.content(
            rx.menu.item(
                rx.hstack(rx.icon("log-out", size=16), rx.text("Sair"), spacing="2"),
                on_click=AuthState.sair,
                color_scheme="red",
            ),
            side="top",
            align="start",
        ),
    )


def sidebar(itens: list[tuple[str, str, str]] | None = None) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(logo(size=30), padding_bottom="1rem"),
            *[
                _nav_link(label, href, icon)
                for label, href, icon in (itens if itens is not None else NAV_ADMIN)
            ],
            rx.spacer(),
            rx.divider(margin_y="0.5rem"),
            user_menu(),
            rx.hstack(
                rx.color_mode.button(),
                rx.text("Clínica Veterinária", size="1", color=rx.color("gray", 9)),
                align="center",
                spacing="2",
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
