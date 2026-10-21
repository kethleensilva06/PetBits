"""Esqueletos de carregamento (change `esqueletos-de-carregamento`).

Blocos cinza que pulsam no formato do que vai aparecer, para a tela não
"pular" quando os dados chegam (D1). Quem chama decide QUANDO mostrar: só no
lugar do "carregando", nunca com dado, vazio ou erro (D2).
"""

import reflex as rx


def _bloco(altura: str, largura: str = "100%", raio: str = "0.5rem") -> rx.Component:
    return rx.skeleton(rx.box(height=altura, width=largura), loading=True,
                       border_radius=raio)


def _aviso(texto: str, *filhos: rx.Component, **estilo) -> rx.Component:
    """O contêiner acessível (D3): o leitor de tela lê o texto escondido."""
    return rx.box(
        # Escondido da tela, lido pelo leitor de tela.
        rx.text.span(texto, position="absolute", width="1px", height="1px",
                     overflow="hidden", clip="rect(0 0 0 0)", white_space="nowrap"),
        *filhos,
        role="status",
        aria_busy="true",
        width="100%",
        **estilo,
    )


def _cartao(com_imagem: bool) -> rx.Component:
    return rx.card(
        rx.vstack(
            _bloco("9rem", raio="0.75rem") if com_imagem else rx.fragment(),
            _bloco("1.1rem", "60%"),
            _bloco("0.8rem", "85%"),
            _bloco("0.8rem", "40%"),
            spacing="2",
            width="100%",
        ),
        width="100%",
    )


def cartoes(texto: str, n: int = 4, colunas=None, com_imagem: bool = True) -> rx.Component:
    """Uma grade de cartões, com as mesmas colunas da tela real (D1)."""
    return _aviso(
        texto,
        rx.grid(
            *[_cartao(com_imagem) for _ in range(n)],
            columns=colunas if colunas is not None else rx.breakpoints(initial="1", md="2"),
            spacing="3",
            width="100%",
        ),
    )


def linhas(texto: str, n: int = 3) -> rx.Component:
    """Uma lista de cartões baixos: agendamentos, pedidos, listas da clínica."""
    return _aviso(
        texto,
        rx.vstack(
            *[rx.card(
                rx.hstack(
                    _bloco("1rem", "4rem"),
                    rx.vstack(_bloco("1rem", "55%"), _bloco("0.8rem", "80%"),
                              spacing="2", width="100%"),
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                width="100%",
            ) for _ in range(n)],
            spacing="2",
            width="100%",
        ),
    )


def perfil(texto: str) -> rx.Component:
    """A foto à esquerda e o formulário à direita, como em Meu perfil."""
    return _aviso(
        texto,
        rx.grid(
            rx.card(rx.vstack(rx.skeleton(rx.box(height="6rem", width="6rem"), loading=True,
                                          border_radius="9999px"),
                              _bloco("1.2rem", "60%"), _bloco("0.8rem", "70%"),
                              _bloco("2rem", "50%"),
                              spacing="3", align="center", width="100%", padding="1rem"),
                    width="100%"),
            rx.card(rx.vstack(_bloco("1.2rem", "30%"),
                              *[_bloco("2.5rem") for _ in range(4)],
                              _bloco("2.5rem", "30%"),
                              spacing="3", width="100%"),
                    width="100%"),
            columns=rx.breakpoints(initial="1", md="1fr 2fr"),
            spacing="4",
            width="100%",
        ),
    )


def fichas(texto: str, n: int = 8) -> rx.Component:
    """Os botões de horário livre da agenda."""
    return _aviso(
        texto,
        rx.flex(*[_bloco("2rem", "4.5rem") for _ in range(n)], wrap="wrap", gap="0.5rem"),
    )
