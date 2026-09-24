"""Página de cadastro de produtos."""

import reflex as rx

from petbits.components import (
    data_table,
    error_banner,
    form_dialog,
    form_field,
    layout,
    money,
    page_toolbar,
    row_actions,
)
from petbits.states.produto_state import ProdutoState

COLUNAS = ["Nome", "Categoria", "Marca", "Unidade", "Preço", "Ações"]


def _row(produto: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(produto["nome"]),
        rx.table.cell(produto["categoria"]),
        rx.table.cell(produto["marca"]),
        rx.table.cell(produto["unidade"]),
        rx.table.cell(money(produto["preco_venda"])),
        rx.table.cell(
            row_actions(
                on_edit=ProdutoState.open_edit(produto),
                on_delete=ProdutoState.delete(produto["id"]),
                descricao_exclusao=(
                    "O produto sai do catálogo. Pedidos que já o incluem "
                    "continuam no histórico."
                ),
            )
        ),
    )


def _dialog() -> rx.Component:
    return form_dialog(
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
        aberto=ProdutoState.show_dialog,
        on_open_change=ProdutoState.set_show_dialog,
        titulo=rx.cond(ProdutoState.editing_id, "Editar produto", "Novo produto"),
        erro=ProdutoState.form_error,
        on_cancel=ProdutoState.close_dialog,
        on_save=ProdutoState.save,
    )


def produtos_page() -> rx.Component:
    return layout(
        page_toolbar(
            search_value=ProdutoState.search,
            on_search_change=ProdutoState.set_search,
            on_new_click=ProdutoState.open_new,
            new_label="Novo produto",
        ),
        error_banner(ProdutoState.load_error),
        data_table(
            COLUNAS,
            ProdutoState.filtered_produtos,
            _row,
            vazio="Nenhum produto cadastrado ainda.",
            busca=ProdutoState.search,
        ),
        _dialog(),
        title="Produtos",
        subtitle="Itens disponíveis para venda no petshop",
    )
