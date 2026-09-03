"""Página de cadastro de produtos."""

import reflex as rx

from petbits.components import empty_state, form_field, layout, page_toolbar, row_actions
from petbits.states.produto_state import ProdutoState


def _row(produto: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(produto["nome"]),
        rx.table.cell(produto["categoria"]),
        rx.table.cell(produto["marca"]),
        rx.table.cell(produto["unidade"]),
        rx.table.cell(f"R$ {produto['preco_venda']}"),
        rx.table.cell(
            row_actions(
                on_edit=ProdutoState.open_edit(produto),
                on_delete=ProdutoState.delete(produto["id"]),
            )
        ),
    )


def _dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(ProdutoState.editing_id, "Editar produto", "Novo produto")
            ),
            rx.vstack(
                form_field(
                    "Nome *",
                    rx.input(
                        value=ProdutoState.nome,
                        on_change=ProdutoState.set_nome,
                        placeholder="Ração premium 15kg",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    form_field(
                        "Categoria",
                        rx.input(
                            value=ProdutoState.categoria,
                            on_change=ProdutoState.set_categoria,
                            placeholder="Alimentação, higiene...",
                            width="100%",
                        ),
                    ),
                    form_field(
                        "Marca",
                        rx.input(
                            value=ProdutoState.marca,
                            on_change=ProdutoState.set_marca,
                            placeholder="Marca do produto",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.hstack(
                    form_field(
                        "Unidade",
                        rx.input(
                            value=ProdutoState.unidade,
                            on_change=ProdutoState.set_unidade,
                            placeholder="un, kg, L",
                            width="100%",
                        ),
                    ),
                    form_field(
                        "Preço de venda *",
                        rx.input(
                            value=ProdutoState.preco_venda,
                            on_change=ProdutoState.set_preco_venda,
                            type="number",
                            step="0.01",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.cond(
                    ProdutoState.form_error,
                    rx.callout(
                        ProdutoState.form_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=ProdutoState.close_dialog,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=ProdutoState.save),
                    justify="end",
                    spacing="3",
                    width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="32rem",
        ),
        open=ProdutoState.show_dialog,
        on_open_change=ProdutoState.set_show_dialog,
    )


def produtos_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ProdutoState.search,
            on_search_change=ProdutoState.set_search,
            on_new_click=ProdutoState.open_new,
            new_label="Novo produto",
        ),
        rx.card(
            rx.cond(
                ProdutoState.filtered_produtos,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Nome"),
                            rx.table.column_header_cell("Categoria"),
                            rx.table.column_header_cell("Marca"),
                            rx.table.column_header_cell("Unidade"),
                            rx.table.column_header_cell("Preço"),
                            rx.table.column_header_cell("Ações"),
                        )
                    ),
                    rx.table.body(rx.foreach(ProdutoState.filtered_produtos, _row)),
                    width="100%",
                ),
                empty_state(
                    rx.cond(
                        ProdutoState.search,
                        "Nenhum resultado para a busca.",
                        "Nenhum produto cadastrado ainda.",
                    )
                ),
            ),
            width="100%",
        ),
        _dialog(),
        title="Produtos",
        subtitle="Itens disponíveis para venda no petshop",
    )
