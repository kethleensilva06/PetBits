"""A página de endereço inexistente (change `pagina-nao-encontrada`).

Sem `on_load` e sem requisição: só a marca, a foto e os caminhos de volta.
"""

import reflex as rx

from petbits.caminhos import no_site
from petbits.visual import marca

FOTO = ("/fotos/outro.webp", "Um coelho branco olhando para o lado, curioso")


def nao_encontrada_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            marca("/", tamanho="6"),
            rx.image(src=no_site(FOTO[0]), alt=FOTO[1], width="14rem", height="14rem",
                     object_fit="cover", border_radius="2rem",
                     box_shadow=f"0 18px 40px -20px {rx.color('teal', 9)}"),
            rx.heading("Página não encontrada", size="7", weight="bold",
                       text_align="center"),
            rx.text("O endereço pode ter mudado ou estar digitado errado. Nada de "
                    "errado com você nem com os seus animais.",
                    size="3", color=rx.color("gray", 11), text_align="center",
                    max_width="28rem"),
            rx.hstack(
                rx.link(rx.button(rx.icon("house", size=16), "Ir ao início", size="3"),
                        href="/"),
                rx.button(rx.icon("arrow-left", size=16), "Voltar", size="3",
                          variant="outline", on_click=rx.call_script("history.back()")),
                spacing="3",
                wrap="wrap",
                justify="center",
            ),
            spacing="5",
            align="center",
            width="100%",
        ),
        min_height="100vh",
        padding="2rem 1rem",
        width="100%",
    )
