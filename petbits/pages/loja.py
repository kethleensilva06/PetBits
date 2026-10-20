"""A loja do cliente e os pedidos dele (change `loja`).

O que a tela soma é estimativa: o total que vale é o que o servidor calcula
no `POST pedidos`, com o preço do catálogo naquele instante.
"""

import reflex as rx

from petbits import esqueletos
from petbits.states.loja_state import ORDENS, LojaState
from petbits.visual import LARGURA_DO_CLIENTE, tela_vazia, titulo_de_pagina, topo_do_cliente


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
            # A foto e o nome abrem o detalhe, como numa loja de verdade.
            rx.image(src=p["imagem"], alt=p["nome"], width="100%", height="10rem",
                     object_fit="cover", border_radius="0.9rem", cursor="zoom-in",
                     on_click=LojaState.abrir_produto(p)),
            rx.hstack(
                rx.badge(p["categoria"], variant="soft", radius="full"),
                rx.cond(p["marca"], rx.text(p["marca"], size="1", color=rx.color("gray", 11))),
                spacing="2",
                align="center",
            ),
            rx.heading(p["nome"], size="3", cursor="pointer",
                       on_click=LojaState.abrir_produto(p)),
            rx.cond(p["unidade"], rx.text(p["unidade"], size="1", color=rx.color("gray", 11))),
            rx.cond(p["descricao"], rx.text(p["descricao"], size="2", color=rx.color("gray", 11))),
            rx.spacer(),
            rx.hstack(
                rx.text(p["preco"], weight="bold", size="4"),
                rx.spacer(),
                rx.text(p["disponivel"], size="1", color=rx.color("gray", 11)),
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


def _detalhe_do_produto() -> rx.Component:
    """Foto grande e tudo sobre o produto (change `fotos-realistas`)."""
    p = LojaState.produto_aberto
    return rx.dialog.root(
        rx.dialog.content(
            rx.grid(
                rx.image(src=p["imagem"], alt=p["nome"], width="100%",
                         height=rx.breakpoints(initial="15rem", sm="22rem"),
                         object_fit="cover", border_radius="1rem"),
                rx.vstack(
                    rx.hstack(
                        rx.badge(p["categoria"], variant="soft", radius="full"),
                        rx.cond(p["marca"], rx.text(p["marca"], size="2",
                                                    color=rx.color("gray", 11))),
                        spacing="2",
                        align="center",
                    ),
                    rx.dialog.title(p["nome"], size="6", margin="0"),
                    rx.cond(p["unidade"], rx.text(p["unidade"], size="2",
                                                  color=rx.color("gray", 11))),
                    rx.cond(p["descricao"], rx.text(p["descricao"], size="3",
                                                    color=rx.color("gray", 11))),
                    rx.spacer(),
                    rx.text(p["preco"], weight="bold", size="7",
                            color=rx.color("teal", 11)),
                    rx.text(p["disponivel"], size="1", color=rx.color("gray", 11)),
                    rx.cond(
                        LojaState.quantidade_do_aberto > 0,
                        rx.badge(rx.icon("shopping-cart", size=12), "No carrinho: ",
                                 LojaState.quantidade_do_aberto, variant="soft",
                                 color_scheme="orange", radius="full"),
                    ),
                    # Quantidade antes de adicionar, até o que ainda cabe no estoque
                    # (change `acabamentos-de-tela`, D4).
                    rx.cond(
                        LojaState.pode_por_mais_no_aberto > 0,
                        rx.hstack(
                            rx.hstack(
                                rx.icon_button(rx.icon("minus", size=14),
                                               on_click=LojaState.menos_um, variant="soft",
                                               size="3", aria_label="Menos um",
                                               disabled=LojaState.qtd_detalhe <= 1),
                                rx.text(LojaState.qtd_detalhe, weight="bold", size="4",
                                        min_width="2rem", text_align="center"),
                                rx.icon_button(rx.icon("plus", size=14),
                                               on_click=LojaState.mais_um, variant="soft",
                                               size="3", aria_label="Mais um",
                                               disabled=LojaState.qtd_detalhe
                                               >= LojaState.pode_por_mais_no_aberto),
                                spacing="2",
                                align="center",
                            ),
                            rx.button(rx.icon("shopping-cart", size=16), "Adicionar",
                                      on_click=LojaState.adicionar_do_detalhe, size="3",
                                      flex="1"),
                            spacing="3",
                            width="100%",
                            align="center",
                        ),
                        rx.text("Todo o estoque disponível já está no seu carrinho.",
                                size="2", color=rx.color("gray", 11)),
                    ),
                    spacing="2",
                    align_items="start",
                    height="100%",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="5",
                width="100%",
            ),
            rx.dialog.close(
                rx.icon_button(rx.icon("x", size=16), variant="ghost", color_scheme="gray",
                               aria_label="Fechar", position="absolute", top="0.75rem",
                               right="0.75rem"),
            ),
            max_width="52rem",
            position="relative",
        ),
        open=LojaState.detalhe_aberto,
        on_open_change=LojaState.set_detalhe_aberto,
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
                rx.text("Seu carrinho está vazio.", size="2", color=rx.color("gray", 11)),
            ),
            # O que a conferência com o estoque mudou (change `comprar-de-novo`).
            rx.cond(LojaState.ajuste_carrinho,
                    rx.callout(LojaState.ajuste_carrinho, icon="info", color_scheme="amber",
                               size="1", width="100%")),
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
                        "pedido.", size="1", color=rx.color("gray", 11)),
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


def _busca_e_filtro() -> rx.Component:
    """Busca pelo nome e filtro por categoria (change `acabamentos-de-tela`, D4)."""
    return rx.hstack(
        rx.input(
            rx.input.slot(rx.icon("search", size=16)),
            placeholder="Buscar produto",
            # Sem rótulo visível: o nome vai só para o leitor de tela (change
            # `acessibilidade`).
            custom_attrs={"aria-label": "Buscar produto"},
            value=LojaState.busca,
            on_change=LojaState.set_busca,
            size="3",
            flex="1",
            min_width="12rem",
        ),
        rx.select(
            LojaState.categorias_da_loja,
            value=rx.cond(LojaState.categoria_filtro, LojaState.categoria_filtro, "Todas"),
            on_change=LojaState.set_categoria_filtro,
            size="3",
        ),
        # A ordem (change `ordenar-a-loja`).
        rx.select(
            ORDENS,
            value=LojaState.ordem,
            on_change=LojaState.set_ordem,
            size="3",
            aria_label="Ordenar",
        ),
        spacing="3",
        width="100%",
        wrap="wrap",
    )


def loja_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            topo_do_cliente("/loja"),
            titulo_de_pagina("Loja", "Rações, petiscos e cuidados para o seu animal."),
            _avisos(),
            rx.cond(LojaState.produtos.length() > 0, _busca_e_filtro()),
            rx.grid(
                rx.cond(
                    LojaState.produtos.length() > 0,
                    rx.cond(
                        LojaState.produtos_visiveis.length() > 0,
                        rx.grid(rx.foreach(LojaState.produtos_visiveis, _produto),
                                columns=rx.breakpoints(initial="1", sm="2"), spacing="3",
                                width="100%"),
                        rx.card(
                            rx.vstack(
                                rx.icon("search-x", size=28, color=rx.color("gray", 11)),
                                rx.text("Nenhum produto encontrado com essa busca.",
                                        color=rx.color("gray", 11)),
                                rx.button("Limpar a busca", on_click=LojaState.limpar_filtros,
                                          variant="soft"),
                                spacing="3",
                                align="center",
                                padding="2rem",
                            ),
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        LojaState.mostrar_carregando,
                        esqueletos.cartoes("Carregando a loja...",
                                           colunas=rx.breakpoints(initial="1", sm="2")),
                        rx.text("Nenhum produto à venda no momento.", color=rx.color("gray", 11)),
                    ),
                ),
                _carrinho(),
                columns=rx.breakpoints(initial="1", md="3fr 1.4fr"),
                spacing="5",
                width="100%",
                align_items="start",
            ),
            _finalizacao(),
            _detalhe_do_produto(),
            spacing="4",
            align_items="start",
            padding_y="2rem",
            width="100%",
        ),
        size=LARGURA_DO_CLIENTE,
    )


def _etapa(e: rx.Var) -> rx.Component:
    """Uma etapa do pedido (change `linha-do-tempo-do-pedido`): a faixa no
    alto diz feita, atual ou por vir."""
    return rx.vstack(
        rx.box(height="4px", width="100%", border_radius="9999px",
               background=rx.cond(e["feita"], rx.color("teal", 9),
                                  rx.cond(e["atual"], rx.color("teal", 6),
                                          rx.color("gray", 4)))),
        rx.hstack(
            rx.cond(e["feita"], rx.icon("circle-check", size=14, color=rx.color("teal", 10)),
                    rx.icon("circle", size=14,
                            color=rx.cond(e["atual"], rx.color("teal", 9),
                                          rx.color("gray", 11)))),
            rx.text(e["rotulo"], size="1",
                    weight=rx.cond(e["atual"], "bold", "regular"),
                    color=rx.cond(e["feita"] | e["atual"], rx.color("gray", 12),
                                  rx.color("gray", 11))),
            spacing="1",
            align="start",
        ),
        spacing="1",
        width="100%",
    )


def _etapas(p: rx.Var) -> rx.Component:
    return rx.cond(
        p["cancelado"].to(bool),
        rx.text("Pedido cancelado. Os itens voltaram ao estoque.", size="1",
                color=rx.color("gray", 11)),
        rx.grid(rx.foreach(p["etapas"].to(list[dict]), _etapa),
                columns=rx.breakpoints(initial="2", sm="4"), spacing="2", width="100%",
                padding_y="0.25rem"),
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
            _etapas(p),
            rx.text(p["quando"], " · ", p["origem"], " · ", p["entrega"], " · ",
                    p["pagamento"], size="1", color=rx.color("gray", 11)),
            rx.cond(p["endereco"], rx.text("Entregar em: ", p["endereco"], size="1",
                                           color=rx.color("gray", 11))),
            rx.foreach(p["itens"].to(list[dict]), lambda i: rx.hstack(
                rx.text(i["texto"], size="2"), rx.spacer(), rx.text(i["linha"], size="2"),
                width="100%")),
            # Os itens de volta ao carrinho (change `comprar-de-novo`).
            rx.button(rx.icon("rotate-ccw", size=14), "Comprar de novo", variant="soft",
                      size="1", margin_top="0.25rem",
                      on_click=LojaState.comprar_de_novo(p["id"])),
            spacing="1",
            width="100%",
            align_items="start",
        ),
        width="100%",
    )


def pedidos_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            topo_do_cliente("/pedidos"),
            titulo_de_pagina("Meus pedidos"),
            rx.cond(LojaState.erro,
                    rx.callout(LojaState.erro, icon="triangle_alert", color_scheme="red",
                               size="1", width="100%")),
            rx.cond(
                LojaState.pedidos.length() > 0,
                rx.vstack(rx.foreach(LojaState.pedidos, _pedido), spacing="2", width="100%"),
                rx.cond(
                    LojaState.mostrar_carregando,
                    esqueletos.linhas("Carregando os seus pedidos..."),
                    # Falhou não é vazio: o erro já está no callout acima.
                    rx.cond(LojaState.erro, rx.fragment(), tela_vazia(
                        "/fotos/vazio-pedidos.webp",
                        "Nenhum pedido por aqui",
                        "Ração, petisco, brinquedo: o que você comprar na loja aparece aqui, "
                        "com a situação de cada pedido.",
                        rx.link(rx.button(rx.icon("shopping-bag", size=16), "Ir à loja",
                                          size="3"), href="/loja"),
                    )),
                ),
            ),
            spacing="4",
            align_items="start",
            padding_y="2rem",
            width="100%",
        ),
        size=LARGURA_DO_CLIENTE,
    )
