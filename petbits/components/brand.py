"""A marca do PetBits.

A patinha é desenhada com primitivas (um retângulo e cinco elipses) em vez de
usar o ícone `paw-print` do lucide. Duas razões: o ícone solto lê como ícone,
não como marca; e assim a mesma forma serve de logo, de favicon e de marca
d'água na tela de login, sempre no mesmo desenho.

Não há rotação em lugar nenhum — o arco dos dedos vem de posicionar os
externos mais baixos e menores que os internos. Isso evita depender de
`transform`, que o Reflex não tipa.
"""

import reflex as rx

# Os quatro dedos e o coxim, em coordenadas do viewBox 32×32.
# Os externos (o 1º e o 4º) são menores e mais baixos: é o que dá o arco.
_DEDOS = [
    {"cx": "8.6", "cy": "13.2", "rx": "2.5", "ry": "3.1"},
    {"cx": "13.6", "cy": "10.6", "rx": "2.6", "ry": "3.4"},
    {"cx": "18.9", "cy": "10.6", "rx": "2.6", "ry": "3.4"},
    {"cx": "23.8", "cy": "13.2", "rx": "2.5", "ry": "3.1"},
]
_COXIM = {"cx": "16.2", "cy": "21.2", "rx": "6.6", "ry": "5.4"}


def _patinha(cor: str, opacidade: str = "1") -> list[rx.Component]:
    """As cinco elipses da pata, na cor pedida."""
    return [
        rx.el.svg.ellipse(fill=cor, fill_opacity=opacidade, **dedo)
        for dedo in _DEDOS
    ] + [rx.el.svg.ellipse(fill=cor, fill_opacity=opacidade, **_COXIM)]


def logo_mark(size: int = 28, invertido: bool = False) -> rx.Component:
    """Só o símbolo: o quadradinho com a pata.

    `invertido=True` tira o fundo e deixa a pata branca — para usar sobre o
    painel jade da tela de login.
    """
    fundo = (
        rx.el.svg.rect(
            width="32", height="32", rx="9", fill=rx.color("jade", 9)
        )
        if not invertido
        else rx.fragment()
    )
    return rx.el.svg(
        fundo,
        *_patinha("white" if not invertido else "white"),
        view_box="0 0 32 32",
        width=f"{size}px",
        height=f"{size}px",
        flex_shrink="0",
    )


def logo(size: int = 28, com_texto: bool = True, invertido: bool = False) -> rx.Component:
    """Símbolo + wordmark.

    O wordmark é bicolor de propósito: "Pet" no cinza mais escuro e "Bits" no
    jade. É o que faz parecer marca em vez de um título ao lado de um ícone.
    """
    if not com_texto:
        return logo_mark(size, invertido)

    cor_pet = "white" if invertido else rx.color("gray", 12)
    cor_bits = rx.color("jade", 11) if not invertido else rx.color("jade", 4)

    return rx.hstack(
        logo_mark(size, invertido),
        rx.hstack(
            rx.text("Pet", color=cor_pet),
            rx.text("Bits", color=cor_bits),
            spacing="0",
            font_family="Nunito, sans-serif",
            font_weight="800",
            font_size=f"{round(size * 0.72)}px",
            letter_spacing="-0.02em",
            line_height="1",
        ),
        spacing="2",
        align="center",
    )


def paw_watermark(size: int = 420, opacidade: float = 0.08) -> rx.Component:
    """A mesma pata, gigante e translúcida, para o fundo da tela de login."""
    return rx.el.svg(
        *_patinha("white", str(opacidade)),
        view_box="0 0 32 32",
        width=f"{size}px",
        height=f"{size}px",
        aria_hidden="true",
    )
