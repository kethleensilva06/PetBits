"""Pequenos componentes de UI reutilizados nas páginas de CRUD."""

import reflex as rx

from .tokens import STATUS_ROTULOS, de_mapa


def status_badge(valor, cores: dict[str, str]) -> rx.Component:
    """Badge de status, com o rótulo legível e a cor do mapa correspondente.

    `cores` é um dos mapas de `tokens.py` (agendamento ou pedido) — o rótulo
    sai sempre de `STATUS_ROTULOS`, que cobre os dois.
    """
    return rx.badge(
        de_mapa(valor, STATUS_ROTULOS, ""),
        color_scheme=de_mapa(valor, cores),
        variant="soft",
        radius="full",
    )


def money(valor) -> rx.Component:
    """Valor em reais, com dígitos de largura fixa para alinhar na coluna."""
    return rx.text(
        "R$ ", valor, size="2", font_variant_numeric="tabular-nums", as_="span"
    )


def stat_card(label: str, value, icon: str, href: str = "") -> rx.Component:
    """Cartão de indicador do painel. Vira link quando recebe `href`."""
    cartao = rx.card(
        rx.hstack(
            rx.box(
                rx.icon(icon, size=22, color=rx.color("accent", 9)),
                padding="0.6rem",
                background=rx.color("accent", 3),
                border_radius="0.6rem",
                display="flex",
            ),
            rx.vstack(
                rx.text(label, size="2", color=rx.color("gray", 10)),
                rx.heading(value, size="7"),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
    )
    if not href:
        return cartao
    return rx.link(cartao, href=href, underline="none", width="100%")


def section_card(titulo: str, *children, acao: rx.Component | None = None) -> rx.Component:
    """Cartão com cabeçalho e, opcionalmente, uma ação à direita do título."""
    cabecalho = rx.hstack(
        rx.heading(titulo, size="4"),
        rx.spacer(),
        acao if acao is not None else rx.fragment(),
        width="100%",
        align="center",
        padding_bottom="0.75rem",
    )
    return rx.card(
        rx.vstack(cabecalho, *children, spacing="0", width="100%"),
        width="100%",
    )


def form_field(label: str, input_component: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color=rx.color("gray", 11)),
        input_component,
        spacing="1",
        width="100%",
        align_items="start",
    )


def confirm_delete(
    gatilho: rx.Component,
    on_confirm,
    titulo: str = "Excluir registro?",
    descricao: str = "Esta ação não pode ser desfeita.",
) -> rx.Component:
    """Envolve um gatilho num diálogo de confirmação antes de excluir."""
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(gatilho),
        rx.alert_dialog.content(
            rx.alert_dialog.title(titulo),
            rx.alert_dialog.description(descricao),
            rx.hstack(
                rx.alert_dialog.cancel(
                    rx.button("Cancelar", variant="soft", color_scheme="gray")
                ),
                rx.alert_dialog.action(
                    rx.button("Excluir", color_scheme="red", on_click=on_confirm)
                ),
                justify="end",
                spacing="3",
                padding_top="1rem",
            ),
            max_width="26rem",
        ),
    )


def row_actions(
    on_edit,
    on_delete,
    confirmar: bool = True,
    descricao_exclusao: str = "Esta ação não pode ser desfeita.",
) -> rx.Component:
    """Editar e excluir de uma linha de tabela.

    A exclusão pede confirmação por padrão: o botão fica a um clique de
    distância de dados que não têm como voltar.
    """
    botao_excluir = rx.icon_button(
        rx.icon("trash-2", size=16),
        variant="soft",
        color_scheme="red",
        size="1",
    )
    return rx.hstack(
        rx.icon_button(
            rx.icon("pencil", size=16),
            on_click=on_edit,
            variant="soft",
            size="1",
        ),
        confirm_delete(botao_excluir, on_delete, descricao=descricao_exclusao)
        if confirmar
        else rx.icon_button(
            rx.icon("trash-2", size=16),
            on_click=on_delete,
            variant="soft",
            color_scheme="red",
            size="1",
        ),
        spacing="2",
    )


def data_table(
    colunas: list[str],
    linhas,
    render_linha,
    vazio: str,
    vazio_busca: str = "Nenhum resultado para a busca.",
    busca=None,
) -> rx.Component:
    """Cartão com a tabela, ou o estado vazio quando não há o que mostrar.

    Substitui o bloco card+tabela+empty_state que era idêntico em oito páginas.
    Quando `busca` é informado, o texto do estado vazio distingue "não há nada
    cadastrado" de "a busca não achou nada".
    """
    sem_dados = (
        rx.cond(busca, vazio_busca, vazio) if busca is not None else vazio
    )
    return rx.card(
        rx.cond(
            linhas,
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        *[rx.table.column_header_cell(c) for c in colunas]
                    )
                ),
                rx.table.body(rx.foreach(linhas, render_linha)),
                width="100%",
                size="2",
            ),
            empty_state(sem_dados),
        ),
        width="100%",
    )


def form_dialog(
    *campos,
    aberto,
    on_open_change,
    titulo,
    erro,
    on_cancel,
    on_save,
    largura: str = "32rem",
    rotulo_salvar: str = "Salvar",
) -> rx.Component:
    """A casca do diálogo de formulário: título, campos, erro e rodapé.

    Os oito diálogos do projeto só diferiam pelos campos — título, callout de
    erro e o par Cancelar/Salvar eram copiados à mão em cada um.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(titulo),
            rx.vstack(
                *campos,
                error_banner(erro),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=on_cancel,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button(rotulo_salvar, on_click=on_save),
                    justify="end",
                    spacing="3",
                    width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3",
                width="100%",
            ),
            max_width=largura,
        ),
        open=aberto,
        on_open_change=on_open_change,
    )


def select_fk(
    rotulo: str,
    opcoes,
    campo_rotulo: str,
    valor,
    on_change,
    placeholder: str,
) -> rx.Component:
    """Select de chave estrangeira.

    As opções são `list[dict]` com `id` e o campo de exibição; o valor
    trafega como string, que é o que o select do Radix entende.
    """
    return form_field(
        rotulo,
        rx.select.root(
            rx.select.trigger(placeholder=placeholder, width="100%"),
            rx.select.content(
                rx.foreach(
                    opcoes,
                    lambda o: rx.select.item(
                        o[campo_rotulo], value=o["id"].to_string()
                    ),
                )
            ),
            value=valor,
            on_change=on_change,
            width="100%",
        ),
    )


def error_banner(message) -> rx.Component:
    """Aviso exibido quando o Xano não responde ou recusa a requisição."""
    return rx.cond(
        message,
        rx.callout(
            message,
            icon="triangle_alert",
            color_scheme="red",
            width="100%",
        ),
    )


def empty_state(message) -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon("inbox", size=32, color=rx.color("gray", 8)),
            rx.text(message, color=rx.color("gray", 9)),
            spacing="2",
        ),
        padding="3rem",
        width="100%",
    )


def page_toolbar(search_value, on_search_change, on_new_click, new_label: str) -> rx.Component:
    return rx.hstack(
        rx.input(
            rx.input.slot(rx.icon("search", size=16)),
            placeholder="Buscar...",
            value=search_value,
            on_change=on_search_change,
            width="20rem",
        ),
        rx.spacer(),
        rx.button(
            rx.icon("plus", size=16),
            new_label,
            on_click=on_new_click,
        ),
        width="100%",
        align="center",
    )
