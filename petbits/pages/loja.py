"""A loja do cliente e os pedidos dele (change `loja`).

O que a tela soma é estimativa: o total que vale é o que o servidor calcula
no `POST pedidos`, com o preço do catálogo naquele instante.
"""

import reflex as rx

from petbits.states.auth_state import AuthState
from petbits.states.loja_state import LojaState


def _topo(atual: str) -> rx.Component:
    def link(rotulo, href):
        return rx.link(rotulo, href=href, size="2",
                       weight="bold" if href == atual else "regular")
    return rx.hstack(
        rx.link(rx.heading("PetBits", size="6"), href="/", underline="none", color="inherit"),
        rx.spacer(),
        link("Meus animais", "/"),
        link("Agendar", "/agenda"),
        link("Loja", "/loja"),
        link("Meus pedidos", "/pedidos"),
        rx.button("Sair", on_click=AuthState.sair, variant="soft", color_scheme="gray",
                  size="2"),
        width="100%",
        align="center",
        spacing="4",
        wrap="wrap",
        padding_bottom="1.5rem",
    )


def _avisos() -> rx.Component:
    return rx.fragment(
        rx.cond(LojaState.aviso,
                rx.callout(LojaState.aviso, icon="circle_check", color_scheme="green",
                           size="1", width="100%")),
        rx.cond(LojaState.erro & ~LojaState.finalizando,
                rx.callout(LojaState.erro, icon="triangle_alert", color_scheme="red",
                           size="1", width="100%")),
    )


def _produto(p: rx.Var) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(p["categoria"], variant="soft", radius="full"),
                rx.cond(p["marca"], rx.text(p["marca"], size="1", color=rx.color("gray", 10))),
                spacing="2",
                align="center",
            ),
            rx.heading(p["nome"], size="3"),
            rx.cond(p["unidade"], rx.text(p["unidade"], size="1", color=rx.color("gray", 10))),
            rx.cond(p["descricao"], rx.text(p["descricao"], size="2", color=rx.color("gray", 11))),
            rx.spacer(),
            rx.hstack(
                rx.text(p["preco"], weight="bold", size="4"),
                rx.spacer(),
                rx.text(p["disponivel"], size="1", color=rx.color("gray", 10)),
                width="100%",
                align="center",
            ),
            rx.button(rx.icon("shopping-cart", size=16), "Adicionar",
                      on_click=LojaState.adicionar(p["id"]), width="100%"),
            spacing="2",
            align_items="start",
            height="100%",
        ),
        width="100%",
    )


def _item_do_carrinho(i: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.text(i["nome"], size="2", flex="1"),
        rx.icon_button(rx.icon("minus", size=14), size="1", variant="soft",
                       on_click=LojaState.tirar(i["id"]), aria_label="Tirar um"),
        rx.text(i["quantidade"], size="2", min_width="1.5rem", text_align="center"),
        rx.icon_button(rx.icon("plus", size=14), size="1", variant="soft",
                       on_click=LojaState.adicionar(i["id"].to(int)),
                       disabled=~i["pode_mais"].to(bool), aria_label="Mais um"),
        rx.text(i["linha"], size="2", min_width="6rem", text_align="right"),
        width="100%",
        align="center",
        spacing="2",
    )


def _carrinho() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(rx.icon("shopping-cart", size=18), rx.heading("Carrinho", size="4"),
                      spacing="2", align="center"),
            rx.cond(
                LojaState.quantidade_no_carrinho > 0,
                rx.vstack(
                    rx.foreach(LojaState.itens_do_carrinho, _item_do_carrinho),
                    rx.divider(),
                    rx.hstack(rx.text("Total estimado", weight="medium"), rx.spacer(),
                              rx.text(LojaState.total_estimado, weight="bold"), width="100%"),
                    rx.button("Finalizar compra", on_click=LojaState.abrir_finalizacao,
                              size="3", width="100%"),
                    spacing="2",
                    width="100%",
                ),
                rx.text("Seu carrinho está vazio.", size="2", color=rx.color("gray", 10)),
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
        position=rx.breakpoints(initial="static", md="sticky"),
        top="1rem",
    )


def _finalizacao() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Finalizar compra"),
            rx.vstack(
                rx.text("Entrega", weight="medium", size="2"),
                rx.radio_group.root(
                    rx.vstack(
                        rx.radio_group.item("Retirada na clínica", value="retirada"),
                        rx.radio_group.item("Entrega no endereço do meu cadastro",
                                            value="endereco"),
                        spacing="1",
                    ),
                    value=LojaState.entrega,
                    on_change=LojaState.set_entrega,
                ),
                rx.text("Pagamento", weight="medium", size="2", padding_top="0.5rem"),
                rx.radio_group.root(
                    rx.vstack(
                        rx.radio_group.item("Pagar na loja (na retirada ou na entrega)",
                                            value="na_loja"),
                        rx.radio_group.item("Pagar online agora", value="online"),
                        spacing="1",
                    ),
                    value=LojaState.forma_pagamento,
                    on_change=LojaState.set_forma_pagamento,
                ),
                rx.cond(
                    LojaState.forma_pagamento == "online",
                    rx.callout(
                        "Pagamento SIMULADO: nenhum valor é cobrado e nenhum dado de "
                        "cartão é pedido. O pedido só fica registrado como pago na sua conta.",
                        icon="info", color_scheme="amber", size="1", width="100%",
                    ),
                ),
                rx.hstack(rx.text("Total estimado"), rx.spacer(),
                          rx.text(LojaState.total_estimado, weight="bold"),
                          width="100%", padding_top="0.5rem"),
                rx.text("O valor final é calculado com o preço do catálogo no momento do "
                        "pedido.", size="1", color=rx.color("gray", 10)),
                rx.cond(LojaState.erro,
                        rx.callout(LojaState.erro, icon="triangle_alert", color_scheme="red",
                                   size="1", width="100%")),
                rx.hstack(
                    rx.button("Voltar", variant="soft", color_scheme="gray",
                              on_click=LojaState.set_finalizando(False)),
                    rx.button("Confirmar pedido", on_click=LojaState.finalizar,
                              disabled=LojaState.enviando),
                    justify="end", spacing="3", width="100%", padding_top="0.5rem",
                ),
                spacing="2",
                width="100%",
                align_items="start",
            ),
            max_width="30rem",
        ),
        open=LojaState.finalizando,
        on_open_change=LojaState.set_finalizando,
    )


def loja_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            _topo("/loja"),
            rx.heading("Loja", size="7"),
            _avisos(),
            rx.grid(
                rx.cond(
                    LojaState.produtos.length() > 0,
                    rx.grid(rx.foreach(LojaState.produtos, _produto),
                            columns=rx.breakpoints(initial="1", sm="2"), spacing="3",
                            width="100%"),
                    rx.cond(
                        LojaState.carregando,
                        rx.hstack(rx.spinner(size="2"), rx.text("Carregando a loja...")),
                        rx.text("Nenhum produto à venda no momento.", color=rx.color("gray", 10)),
                    ),
                ),
                _carrinho(),
                columns=rx.breakpoints(initial="1", md="3fr 1.4fr"),
                spacing="5",
                width="100%",
                align_items="start",
            ),
            _finalizacao(),
            spacing="4",
            align_items="start",
            padding_y="3rem",
            width="100%",
        ),
        size="4",
    )


def _pedido(p: rx.Var) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Pedido nº ", p["id"], weight="bold"),
                rx.badge(p["situacao"], radius="full",
                         color_scheme=rx.cond(p["cancelado"].to(bool), "gray", "teal")),
                rx.spacer(),
                rx.text(p["total"], weight="bold"),
                width="100%",
                align="center",
                wrap="wrap",
            ),
            rx.text(p["quando"], " · ", p["entrega"], " · ", p["pagamento"], size="1",
                    color=rx.color("gray", 10)),
            rx.cond(p["endereco"], rx.text("Entregar em: ", p["endereco"], size="1",
                                           color=rx.color("gray", 10))),
            rx.foreach(p["itens"].to(list[dict]), lambda i: rx.hstack(
                rx.text(i["texto"], size="2"), rx.spacer(), rx.text(i["linha"], size="2"),
                width="100%")),
            spacing="1",
            width="100%",
            align_items="start",
        ),
        width="100%",
    )


def pedidos_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            _topo("/pedidos"),
            rx.heading("Meus pedidos", size="7"),
            rx.cond(LojaState.erro,
                    rx.callout(LojaState.erro, icon="triangle_alert", color_scheme="red",
                               size="1", width="100%")),
            rx.cond(
                LojaState.pedidos.length() > 0,
                rx.vstack(rx.foreach(LojaState.pedidos, _pedido), spacing="2", width="100%"),
                rx.cond(
                    LojaState.carregando,
                    rx.hstack(rx.spinner(size="2"), rx.text("Carregando...")),
                    rx.hstack(rx.text("Você ainda não fez nenhum pedido.",
                                      color=rx.color("gray", 10)),
                              rx.link("Ir para a loja", href="/loja")),
                ),
            ),
            spacing="4",
            align_items="start",
            padding_y="3rem",
            width="100%",
        ),
        size="3",
    )
