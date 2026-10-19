"""Identidade visual do PetBits: tema, marca e cabeçalhos (change `identidade-visual`).

Nada aqui pergunta ao backend: o cabeçalho usa só o que já está no
`AuthState` (D3). Uma tela que precisasse de requisição para desenhar o topo
gastaria orçamento da instância do Xano a cada clique no menu.
"""

import reflex as rx

from petbits.states.auth_state import AuthState
from petbits.states.loja_state import LojaState

TEMA = rx.theme(
    appearance="inherit",
    accent_color="teal",
    gray_color="sand",
    radius="large",
)

FOLHAS_DE_ESTILO = [
    "https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap",
    "/estilo.css",
]

AREAS_DO_CLIENTE = [
    ("/inicio", "Meus animais", "paw-print"),
    ("/agenda", "Agendar", "calendar"),
    ("/loja", "Loja", "shopping-bag"),
    ("/pedidos", "Meus pedidos", "receipt"),
]


def marca(href: str | None = None, tamanho: str = "5") -> rx.Component:
    """O selo com a patinha e o nome. Com `href`, leva à tela inicial da área."""
    grande = tamanho in ("7", "8", "9")
    selo = rx.center(
        rx.icon("paw-print", size=30 if grande else 18, color="white"),
        width="3.5rem" if grande else "2.1rem",
        height="3.5rem" if grande else "2.1rem",
        border_radius="30%",
        background=f"linear-gradient(135deg, {rx.color('teal', 9)}, {rx.color('teal', 11)})",
        box_shadow=f"0 4px 14px -4px {rx.color('teal', 8)}",
        flex_shrink="0",
    )
    conteudo = rx.hstack(
        selo,
        rx.heading("Pet", rx.text.span("Bits", color=rx.color("teal", 10)),
                   size=tamanho, weight="bold"),
        spacing="3" if grande else "2",
        align="center",
    )
    if href is None:
        return conteudo
    return rx.link(conteudo, href=href, underline="none", color="inherit")


def pilula(rotulo: str, icone: str, href: str, ativo: bool) -> rx.Component:
    """Item de menu. A tela atual fica preenchida; as outras, só texto."""
    return rx.link(
        rx.hstack(
            rx.icon(icone, size=15),
            rx.text(rotulo, size="2", weight="medium" if ativo else "regular"),
            spacing="2",
            align="center",
        ),
        href=href,
        underline="none",
        padding="0.4rem 0.85rem",
        border_radius="9999px",
        color=rx.color("teal", 11) if ativo else rx.color("gray", 11),
        background=rx.color("teal", 4) if ativo else "transparent",
        _hover={"background": rx.color("teal", 3) if ativo else rx.color("gray", 3)},
        white_space="nowrap",
    )


def barra(*conteudo) -> rx.Component:
    """A faixa do topo, translúcida sobre o fundo do tema."""
    return rx.hstack(
        *conteudo,
        width="100%",
        align="center",
        # No celular, espaços menores: com o sol/lua, o carrinho, o avatar e o
        # sair, a faixa tem de caber numa linha (change `tema-claro-escuro`).
        spacing=rx.breakpoints(initial="2", sm="3"),
        wrap="wrap",
        padding=rx.breakpoints(initial="0.6rem 0.7rem", sm="0.75rem 1rem"),
        border_radius="1rem",
        background=rx.color("gray", 1),
        border=f"1px solid {rx.color('gray', 4)}",
        box_shadow=f"0 1px 2px {rx.color('gray', 3)}",
    )


def botao_tema(**props) -> rx.Component:
    """Sol/lua: alterna claro e escuro (change `tema-claro-escuro`, D1 e D2).

    Usa o modo de cor do Reflex, que o tema (`appearance="inherit"`) segue e
    que fica guardado no navegador. Sem escolha, vale o do sistema.
    """
    return rx.icon_button(
        rx.color_mode_cond(rx.icon("moon", size=16), rx.icon("sun", size=16)),
        on_click=rx.toggle_color_mode,
        variant="soft",
        color_scheme="gray",
        size="2",
        aria_label="Alternar entre claro e escuro",
        title="Claro ou escuro",
        **props,
    )


def sair() -> rx.Component:
    # No celular fica só o ícone, para o topo caber numa linha (change
    # `acabamentos-de-tela`, D3); o nome continua para leitor de tela.
    return rx.button(rx.icon("log-out", size=15),
                     rx.text("Sair", display=rx.breakpoints(initial="none", sm="inline")),
                     on_click=AuthState.sair, variant="soft", color_scheme="gray", size="2",
                     aria_label="Sair")


def topo_do_cliente(atual: str) -> rx.Component:
    """O cabeçalho único da área do cliente (casa, agenda, loja, pedidos)."""
    return rx.vstack(
        barra(
            marca("/inicio"),
            rx.spacer(),
            rx.badge(AuthState.papel_exibido, variant="soft", color_scheme="orange",
                     radius="full", display=rx.breakpoints(initial="none", sm="inline-flex")),
            botao_tema(),
            # O carrinho em qualquer tela do cliente (change `acabamentos-de-tela`,
            # D4): o número sai do LojaState, sem requisição.
            rx.link(
                rx.box(
                    rx.icon_button(rx.icon("shopping-cart", size=18), variant="soft",
                                   size="2", aria_label="Carrinho"),
                    rx.cond(
                        LojaState.quantidade_no_carrinho > 0,
                        rx.badge(LojaState.quantidade_no_carrinho, color_scheme="orange",
                                 variant="solid", radius="full", position="absolute",
                                 top="-0.4rem", right="-0.4rem", size="1"),
                    ),
                    position="relative",
                ),
                href="/loja",
                title="Carrinho",
            ),
            # Tocar no próprio avatar abre o perfil (change `perfil-e-fotos`, D6).
            rx.link(
                rx.avatar(src=AuthState.usuario_foto, fallback=AuthState.iniciais,
                          radius="full", size="3", color_scheme="teal",
                          variant="solid"),
                href="/perfil",
                aria_label="Meu perfil",
                title="Meu perfil",
                border_radius="9999px",
                box_shadow=(f"0 0 0 2px {rx.color('teal', 8)}" if atual == "/perfil"
                            else "none"),
            ),
            sair(),
        ),
        rx.hstack(
            *[pilula(rotulo, icone, href, href == atual)
              for href, rotulo, icone in AREAS_DO_CLIENTE],
            spacing="1",
            wrap="wrap",
            width="100%",
        ),
        spacing="3",
        width="100%",
        padding_bottom="1rem",
    )


def titulo_de_pagina(titulo, subtitulo=None) -> rx.Component:
    return rx.vstack(
        rx.heading(titulo, size="7", weight="bold"),
        rx.text(subtitulo, color=rx.color("gray", 11), size="2")
        if subtitulo is not None else rx.fragment(),
        spacing="1",
        align_items="start",
    )


def tela_vazia(imagem: str, titulo: str, texto: str, acao: rx.Component) -> rx.Component:
    """Ilustração, o que fazer e o botão para fazer (change `cliente-ilustrado`, D4).

    Quem chama decide QUANDO mostrar: nunca enquanto carrega nem quando falhou.
    """
    return rx.card(
        rx.vstack(
            rx.image(src=imagem, alt="", width="15rem", max_width="80%", height="10rem",
                     object_fit="cover", border_radius="1.25rem"),
            rx.heading(titulo, size="5", weight="bold", text_align="center"),
            rx.text(texto, size="2", color=rx.color("gray", 11), text_align="center",
                    max_width="26rem"),
            acao,
            spacing="3",
            align="center",
            width="100%",
            padding="2rem 1rem",
        ),
        width="100%",
    )
