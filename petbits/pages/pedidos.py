"""Página de pedidos de produtos e seus itens."""

import reflex as rx

from petbits.components import (
    STATUS_PEDIDO_CORES,
    empty_state,
    error_banner,
    form_field,
    layout,
    money,
    page_toolbar,
    row_actions,
    status_badge,
)
from petbits.models import STATUS_PEDIDO
from petbits.states.pedido_state import PedidoState


def _row(pedido: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(f"#{pedido['id']}"),
        rx.table.cell(pedido["cliente_nome"]),
        rx.table.cell(pedido["data_pedido"]),
        rx.table.cell(status_badge(pedido["status"], STATUS_PEDIDO_CORES)),
        rx.table.cell(money(pedido["valor_total"])),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    rx.icon("list", size=16),
                    "Itens",
                    on_click=PedidoState.open_itens(pedido),
                    variant="soft",
                    size="1",
                ),
                row_actions(
                    on_edit=PedidoState.open_edit(pedido),
                    on_delete=PedidoState.delete(pedido["id"]),
                ),
                spacing="2",
            )
        ),
    )


def _item_row(item: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(item["produto_nome"]),
        rx.table.cell(item["quantidade"]),
        rx.table.cell(f"R$ {item['valor_unitario']}"),
        rx.table.cell(f"R$ {item['valor_total']}"),
        rx.table.cell(
            rx.icon_button(
                rx.icon("trash-2", size=16),
                on_click=PedidoState.remove_item(item["id"]),
                variant="soft",
                color_scheme="red",
                size="1",
            )
        ),
    )


def _pedido_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(PedidoState.editing_id, "Editar pedido", "Novo pedido")
            ),
            rx.vstack(
                form_field(
                    "Cliente *",
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Selecione o cliente", width="100%"
                        ),
                        rx.select.content(
                            rx.foreach(
                                PedidoState.cliente_options,
                                lambda c: rx.select.item(
                                    c["nome"], value=c["id"].to_string()
                                ),
                            )
                        ),
                        value=PedidoState.id_cliente,
                        on_change=PedidoState.set_id_cliente,
                        width="100%",
                    ),
                ),
                form_field(
                    "Status",
                    rx.select(
                        STATUS_PEDIDO,
                        value=PedidoState.status,
                        on_change=PedidoState.set_status,
                        width="100%",
                    ),
                ),
                rx.cond(
                    PedidoState.form_error,
                    rx.callout(
                        PedidoState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.text(
                    "O valor total é calculado automaticamente a partir dos itens do pedido.",
                    size="1",
                    color=rx.color("gray", 10),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=PedidoState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=PedidoState.save),
                    justify="end",
                    spacing="3",
                    width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="30rem",
        ),
        open=PedidoState.show_dialog,
        on_open_change=PedidoState.set_show_dialog,
    )


def _itens_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Itens do pedido"),
            rx.dialog.description(
                f"Cliente: {PedidoState.selected_pedido_cliente}",
                color=rx.color("gray", 10),
            ),
            rx.vstack(
                rx.hstack(
                    form_field(
                        "Produto",
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Selecione o produto", width="100%"
                            ),
                            rx.select.content(
                                rx.foreach(
                                    PedidoState.produto_options,
                                    lambda p: rx.select.item(
                                        p["nome"], value=p["id"].to_string()
                                    ),
                                )
                            ),
                            value=PedidoState.item_id_produto,
                            on_change=PedidoState.set_item_id_produto,
                            width="100%",
                        ),
                    ),
                    form_field(
                        "Qtd.",
                        rx.input(
                            value=PedidoState.item_quantidade,
                            on_change=PedidoState.set_item_quantidade,
                            type="number",
                            min="1",
                            width="6rem",
                        ),
                    ),
                    rx.button(
                        rx.icon("plus", size=16),
                        "Adicionar",
                        on_click=PedidoState.add_item,
                        margin_top="1.4rem",
                    ),
                    spacing="3",
                    width="100%",
                    align="start",
                ),
                rx.cond(
                    PedidoState.item_error,
                    rx.callout(
                        PedidoState.item_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.cond(
                    PedidoState.itens,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Produto"),
                                rx.table.column_header_cell("Qtd."),
                                rx.table.column_header_cell("Unitário"),
                                rx.table.column_header_cell("Subtotal"),
                                rx.table.column_header_cell(""),
                            )
                        ),
                        rx.table.body(rx.foreach(PedidoState.itens, _item_row)),
                        width="100%",
                    ),
                    empty_state("Nenhum item adicionado a este pedido."),
                ),
                rx.hstack(
                    rx.spacer(),
                    rx.text("Total: ", weight="bold"),
                    rx.text(f"R$ {PedidoState.itens_total}", weight="bold"),
                    width="100%",
                ),
                rx.hstack(
                    rx.spacer(),
                    rx.button("Fechar", on_click=PedidoState.close_itens, variant="soft"),
                    width="100%",
                ),
                spacing="3",
                width="100%",
                padding_top="1rem",
            ),
            max_width="44rem",
        ),
        open=PedidoState.show_itens_dialog,
        on_open_change=PedidoState.set_show_itens_dialog,
    )


def pedidos_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=PedidoState.search,
            on_search_change=PedidoState.set_search,
            on_new_click=PedidoState.open_new,
            new_label="Novo pedido",
        ),
        error_banner(PedidoState.load_error),
        rx.card(
            rx.cond(
                PedidoState.filtered_pedidos,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Pedido"),
                            rx.table.column_header_cell("Cliente"),
                            rx.table.column_header_cell("Data"),
                            rx.table.column_header_cell("Status"),
                            rx.table.column_header_cell("Valor total"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(rx.foreach(PedidoState.filtered_pedidos, _row)),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        PedidoState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum pedido registrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _pedido_dialog(),
        _itens_dialog(),
        title="Pedidos",
        subtitle="Vendas de produtos do petshop",
    )
