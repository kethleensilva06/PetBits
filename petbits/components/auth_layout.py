"""A casca das telas de login e cadastro.

Duas colunas: à esquerda o painel da marca, à direita o formulário. O painel
some abaixo de `md` — num celular ele empurraria o formulário para fora da
primeira dobra, e quem abre o site quer entrar, não ler a proposta de valor.

O formulário mora dentro de um `rx.form` para o Enter enviar: numa tela de
login, obrigar o clique no botão é o tipo de atrito que ninguém reporta como
bug mas todo mundo sente.
"""

import reflex as rx

from .brand import logo, paw_watermark

# O que o painel da esquerda promete. Fica aqui, e não na página, porque é o
# mesmo texto no login e no cadastro.
_DESTAQUES = [
    ("calendar-check", "Consultas e banhos", "Agende em poucos cliques e acompanhe o histórico."),
    ("paw-print", "Seus pets", "Ficha, vacinas e prontuário sempre à mão."),
    ("shield-check", "Cuidado de verdade", "Cada atendimento registrado pela equipe da clínica."),
]


def _destaque(icone: str, titulo: str, texto: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.icon(icone, size=18, color="white"),
            padding="0.55rem",
            background="rgba(255,255,255,0.18)",
            border_radius="0.6rem",
            display="flex",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(titulo, size="3", weight="bold", color="white"),
            rx.text(texto, size="2", color="rgba(255,255,255,0.82)"),
            spacing="0",
            align_items="start",
        ),
        spacing="3",
        align="start",
        width="100%",
    )


def _painel_marca() -> rx.Component:
    return rx.box(
        # A marca d'água é decorativa e precisa ficar atrás do texto sem
        # empurrar o layout: daí `position="absolute"` e o overflow escondido.
        rx.box(
            paw_watermark(size=460, opacidade=0.10),
            position="absolute",
            right="-6rem",
            bottom="-8rem",
            pointer_events="none",
        ),
        rx.vstack(
            logo(size=34, invertido=True),
            rx.spacer(),
            rx.vstack(
                rx.heading(
                    "O cuidado do seu pet, organizado.",
                    size="8",
                    color="white",
                    font_family="Nunito, sans-serif",
                    line_height="1.15",
                ),
                rx.text(
                    "PetBits reúne a agenda, o prontuário e as compras da "
                    "clínica em um só lugar.",
                    size="3",
                    color="rgba(255,255,255,0.85)",
                ),
                spacing="3",
                align_items="start",
                padding_bottom="2rem",
            ),
            rx.vstack(
                *[_destaque(i, t, d) for i, t, d in _DESTAQUES],
                spacing="4",
                width="100%",
            ),
            height="100%",
            width="100%",
            align_items="start",
            spacing="4",
        ),
        display=rx.breakpoints(initial="none", md="block"),
        position="relative",
        overflow="hidden",
        width="50%",
        min_height="100vh",
        padding="3rem",
        background=(
            f"linear-gradient(150deg, {rx.color('jade', 10)} 0%, "
            f"{rx.color('jade', 11)} 55%, {rx.color('jade', 12)} 100%)"
        ),
    )


def auth_layout(
    *campos,
    titulo: str,
    subtitulo: str,
    erro,
    enviando,
    rotulo_envio: str,
    on_submit,
    rodape: rx.Component,
) -> rx.Component:
    """Monta uma tela de porta de entrada.

    `on_submit` recebe o dict do formulário, que ignoramos: os valores já
    estão no State pelos `on_change`. O `rx.form` está aqui pelo Enter.
    """
    return rx.hstack(
        _painel_marca(),
        rx.center(
            rx.vstack(
                # No celular o painel jade não aparece, então a marca precisa
                # aparecer aqui — senão a tela de login não diz de quem é.
                rx.box(
                    logo(size=30),
                    display=rx.breakpoints(initial="block", md="none"),
                    padding_bottom="0.5rem",
                ),
                rx.vstack(
                    rx.heading(titulo, size="7", font_family="Nunito, sans-serif"),
                    rx.text(subtitulo, size="2", color=rx.color("gray", 10)),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
                rx.form(
                    rx.vstack(
                        *campos,
                        rx.cond(
                            erro,
                            rx.callout(
                                erro,
                                icon="triangle_alert",
                                color_scheme="red",
                                size="1",
                                width="100%",
                            ),
                        ),
                        rx.button(
                            rx.cond(enviando, rx.spinner(size="2"), rx.fragment()),
                            rotulo_envio,
                            type="submit",
                            size="3",
                            width="100%",
                            disabled=enviando,
                            margin_top="0.5rem",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=on_submit,
                    reset_on_submit=False,
                    width="100%",
                ),
                rodape,
                spacing="4",
                width="100%",
                max_width="24rem",
                align_items="start",
            ),
            width=rx.breakpoints(initial="100%", md="50%"),
            min_height="100vh",
            padding="2rem 1.5rem",
        ),
        spacing="0",
        width="100%",
        align_items="stretch",
    )


def campo_senha(
    rotulo: str,
    valor,
    on_change,
    mostrar,
    on_toggle,
    placeholder: str = "Sua senha",
) -> rx.Component:
    """Campo de senha com o olhinho de mostrar/esconder.

    Esconder por padrão protege de quem olha por cima do ombro; poder mostrar
    evita o erro de digitação que, no cadastro, custa uma conta não criada.
    """
    from .ui import form_field

    return form_field(
        rotulo,
        rx.input(
            rx.input.slot(rx.icon("lock", size=16)),
            rx.input.slot(
                rx.icon_button(
                    rx.cond(mostrar, rx.icon("eye-off", size=16), rx.icon("eye", size=16)),
                    on_click=on_toggle,
                    type="button",
                    variant="ghost",
                    size="1",
                    color_scheme="gray",
                ),
                side="right",
            ),
            placeholder=placeholder,
            type=rx.cond(mostrar, "text", "password"),
            value=valor,
            on_change=on_change,
            size="3",
            width="100%",
        ),
    )
