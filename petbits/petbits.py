"""PetBits — aplicação Reflex.

Ponto de partida em branco, conforme o Apêndice B (`reflex init` → "A blank
Reflex app"). O conteúdo desta aplicação será construído change por change,
pelo fluxo do OpenSpec: nenhuma página, State ou componente deve aparecer
aqui sem uma change correspondente em `openspec/changes/`.
"""

import reflex as rx


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("PetBits", size="8"),
            rx.text(
                "Sistema de gestão para clínica veterinária e petshop.",
                color=rx.color("gray", 11),
            ),
            rx.text(
                "Ainda sem funcionalidades: cada uma entra por uma change do "
                "OpenSpec.",
                size="2",
                color=rx.color("gray", 10),
            ),
            spacing="3",
            align="start",
            padding_y="4rem",
        )
    )


app = rx.App()
app.add_page(index, route="/", title="PetBits")
