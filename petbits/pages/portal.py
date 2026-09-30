"""As seis telas do portal do tutor.

Elas moram num arquivo só porque compartilham quase tudo — o cartão de pet, o
badge de status, o cabeçalho de seção — e separá-las em seis arquivos com
dois imports cruzados cada um não organizaria nada.

O que distingue o portal do painel não é o layout, é o que **falta**: não há
`page_toolbar` com busca, não há `row_actions` de excluir, e três das seis
telas não têm nenhuma ação de escrita. A ausência é o que comunica que ali se
acompanha, não se administra.
"""

import reflex as rx

from petbits.components import (
    STATUS_AGENDAMENTO_CORES,
    STATUS_PEDIDO_CORES,
    empty_state,
    error_banner,
    form_field,
    layout_cliente,
    money,
    section_card,
    status_badge,
)
from petbits.states.auth_state import AuthState
from petbits.states.portal_state import PortalState

# ----------------------------------------------------------------------
# peças compartilhadas
# ----------------------------------------------------------------------


def _pet_card(pet: dict, com_editar: bool = True) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.box(
                rx.icon("paw-print", size=22, color=rx.color("jade", 9)),
                padding="0.7rem",
                background=rx.color("jade", 3),
                border_radius="0.75rem",
                display="flex",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.hstack(
                    rx.heading(pet["nome"], size="4"),
                    rx.badge(pet["especie"], variant="soft", radius="full"),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(
                    pet["raca"],
                    size="2",
                    color=rx.color("gray", 10),
                ),
                rx.hstack(
                    rx.hstack(
                        rx.icon("cake", size=14, color=rx.color("gray", 9)),
                        rx.text(pet["idade"], size="1", color=rx.color("gray", 10)),
                        spacing="1",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("weight", size=14, color=rx.color("gray", 9)),
                        rx.text(
                            pet["peso"],
                            " kg",
                            size="1",
                            color=rx.color("gray", 10),
                        ),
                        spacing="1",
                        align="center",
                    ),
                    spacing="4",
                    padding_top="0.25rem",
                ),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            rx.spacer(),
            rx.cond(
                com_editar,
                rx.icon_button(
                    rx.icon("pencil", size=16),
                    on_click=lambda: PortalState.editar_pet(pet["id"]),
                    variant="soft",
                    size="1",
                ),
                rx.fragment(),
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def _pet_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(PortalState.pet_editing_id, "Editar pet", "Novo pet")
            ),
            rx.vstack(
                form_field(
                    "Nome",
                    rx.input(
                        placeholder="Nome do pet",
                        value=PortalState.pet_nome,
                        on_change=PortalState.set_pet_nome,
                        width="100%",
                    ),
                ),
                rx.hstack(
                    form_field(
                        "Espécie",
                        rx.input(
                            placeholder="Cão, gato...",
                            value=PortalState.pet_especie,
                            on_change=PortalState.set_pet_especie,
                            width="100%",
                        ),
                    ),
                    form_field(
                        "Raça",
                        rx.input(
                            placeholder="Raça",
                            value=PortalState.pet_raca,
                            on_change=PortalState.set_pet_raca,
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                    align="start",
                ),
                rx.hstack(
                    form_field(
                        "Nascimento",
                        rx.input(
                            type="date",
                            value=PortalState.pet_data_nascimento,
                            on_change=PortalState.set_pet_data_nascimento,
                            width="100%",
                        ),
                    ),
                    form_field(
                        "Peso (kg)",
                        rx.input(
                            placeholder="0.0",
                            value=PortalState.pet_peso,
                            on_change=PortalState.set_pet_peso,
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                    align="start",
                ),
                form_field(
                    "Observações",
                    rx.text_area(
                        placeholder="Alergias, cuidados especiais...",
                        value=PortalState.pet_observacoes,
                        on_change=PortalState.set_pet_observacoes,
                        width="100%",
                    ),
                ),
                error_banner(PortalState.pet_error),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=PortalState.fechar_pet,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    rx.button("Salvar", on_click=PortalState.salvar_pet),
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
        open=PortalState.show_pet_dialog,
        on_open_change=PortalState.set_show_pet_dialog,
    )


# ----------------------------------------------------------------------
# /portal
# ----------------------------------------------------------------------


def portal_page() -> rx.Component:
    proxima = rx.cond(
        PortalState.proxima_consulta,
        rx.card(
            rx.hstack(
                rx.box(
                    rx.icon("calendar-check", size=22, color=rx.color("jade", 9)),
                    padding="0.7rem",
                    background=rx.color("jade", 3),
                    border_radius="0.75rem",
                    display="flex",
                ),
                rx.vstack(
                    rx.text(
                        "Sua próxima consulta",
                        size="1",
                        color=rx.color("gray", 10),
                    ),
                    rx.heading(PortalState.proxima_consulta, size="4"),
                    rx.text(
                        PortalState.proxima_consulta_pet,
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    spacing="0",
                    align_items="start",
                ),
                rx.spacer(),
                rx.link(
                    rx.button("Ver consultas", variant="soft"),
                    href="/portal/consultas",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            width="100%",
        ),
        rx.card(
            rx.vstack(
                rx.icon("calendar-plus", size=28, color=rx.color("gray", 8)),
                rx.text("Nenhuma consulta marcada.", color=rx.color("gray", 10)),
                rx.link(
                    rx.button(rx.icon("plus", size=16), "Marcar consulta"),
                    href="/portal/agendar",
                ),
                spacing="3",
                align="center",
                width="100%",
                padding="1.5rem",
            ),
            width="100%",
        ),
    )

    return layout_cliente(
        error_banner(PortalState.load_error),
        rx.heading(
            "Olá, " + AuthState.primeiro_nome + "!",
            size="7",
            font_family="Nunito, sans-serif",
        ),
        rx.text(
            "Acompanhe aqui tudo o que acontece com os seus pets.",
            color=rx.color("gray", 10),
        ),
        proxima,
        section_card(
            "Meus pets",
            rx.cond(
                PortalState.pets,
                rx.grid(
                    rx.foreach(
                        PortalState.pets,
                        lambda pet: _pet_card(pet, com_editar=False),
                    ),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="3",
                    width="100%",
                ),
                empty_state("Você ainda não cadastrou nenhum pet."),
            ),
            acao=rx.link(
                rx.button(rx.icon("plus", size=16), "Cadastrar pet", size="2"),
                href="/portal/pets",
            ),
        ),
    )


# ----------------------------------------------------------------------
# /portal/pets
# ----------------------------------------------------------------------


def portal_pets_page() -> rx.Component:
    return layout_cliente(
        error_banner(PortalState.load_error),
        rx.hstack(
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=16),
                "Novo pet",
                on_click=PortalState.novo_pet,
            ),
            width="100%",
        ),
        rx.cond(
            PortalState.pets,
            rx.grid(
                rx.foreach(PortalState.pets, _pet_card),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="3",
                width="100%",
            ),
            empty_state("Você ainda não cadastrou nenhum pet."),
        ),
        _pet_dialog(),
        title="Meus pets",
        subtitle="Os bichos que a clínica acompanha por você.",
    )


# ----------------------------------------------------------------------
# /portal/agendar
# ----------------------------------------------------------------------


def _cartao_dia(dia: dict) -> rx.Component:
    ativo = PortalState.ag_dia == dia["valor"]
    return rx.box(
        rx.vstack(
            rx.text(
                dia["semana"],
                size="1",
                color=rx.cond(ativo, "white", rx.color("gray", 10)),
            ),
            rx.text(
                dia["dia"],
                size="5",
                weight="bold",
                color=rx.cond(ativo, "white", rx.color("gray", 12)),
            ),
            rx.text(
                dia["mes"],
                size="1",
                color=rx.cond(ativo, "rgba(255,255,255,0.8)", rx.color("gray", 10)),
            ),
            spacing="0",
            align="center",
        ),
        on_click=lambda: PortalState.set_ag_dia(dia["valor"]),
        padding="0.6rem 0.9rem",
        border_radius="0.75rem",
        border=f"1px solid {rx.color('gray', 6)}",
        background=rx.cond(ativo, rx.color("jade", 9), "transparent"),
        cursor="pointer",
        flex_shrink="0",
        min_width="4rem",
        _hover={"border_color": rx.color("jade", 8)},
    )


def _cartao_horario(horario: dict) -> rx.Component:
    ativo = PortalState.ag_hora == horario["valor"]
    return rx.button(
        horario["valor"],
        on_click=lambda: PortalState.set_ag_hora(horario["valor"]),
        variant=rx.cond(ativo, "solid", "outline"),
        color_scheme=rx.cond(horario["livre"], "jade", "gray"),
        disabled=~horario["livre"],
        size="2",
    )


def _cartao_servico(servico: dict) -> rx.Component:
    ativo = PortalState.ag_servico == servico["id"].to_string()
    return rx.box(
        rx.vstack(
            rx.text(servico["nome"], size="2", weight="medium"),
            rx.hstack(
                rx.text(
                    "R$ ", servico["preco"], size="1", color=rx.color("gray", 10)
                ),
                rx.text("·", size="1", color=rx.color("gray", 8)),
                rx.text(
                    servico["duracao"],
                    " min",
                    size="1",
                    color=rx.color("gray", 10),
                ),
                spacing="1",
            ),
            spacing="1",
            align_items="start",
        ),
        on_click=lambda: PortalState.set_ag_servico(servico["id"].to_string()),
        padding="0.75rem 1rem",
        border_radius="0.75rem",
        border=f"1px solid {rx.cond(ativo, rx.color('jade', 8), rx.color('gray', 6))}",
        background=rx.cond(ativo, rx.color("jade", 3), "transparent"),
        cursor="pointer",
        width="100%",
        _hover={"border_color": rx.color("jade", 8)},
    )


def portal_agendar_page() -> rx.Component:
    return layout_cliente(
        error_banner(PortalState.load_error),
        rx.cond(
            PortalState.ag_sucesso,
            rx.callout(
                PortalState.ag_sucesso,
                icon="circle_check",
                color_scheme="jade",
                width="100%",
            ),
        ),
        rx.cond(
            PortalState.pet_opcoes,
            rx.vstack(
                section_card(
                    "1. Para qual pet?",
                    rx.grid(
                        rx.foreach(
                            PortalState.pet_opcoes,
                            lambda pet: rx.box(
                                rx.hstack(
                                    rx.icon("paw-print", size=16),
                                    rx.text(pet["nome"], size="2", weight="medium"),
                                    spacing="2",
                                    align="center",
                                ),
                                on_click=lambda: PortalState.set_ag_pet(
                                    pet["id"].to_string()
                                ),
                                padding="0.75rem 1rem",
                                border_radius="0.75rem",
                                border=f"1px solid {rx.cond(PortalState.ag_pet == pet['id'].to_string(), rx.color('jade', 8), rx.color('gray', 6))}",
                                background=rx.cond(
                                    PortalState.ag_pet == pet["id"].to_string(),
                                    rx.color("jade", 3),
                                    "transparent",
                                ),
                                cursor="pointer",
                                _hover={"border_color": rx.color("jade", 8)},
                            ),
                        ),
                        columns=rx.breakpoints(initial="1", sm="2", md="3"),
                        spacing="2",
                        width="100%",
                    ),
                ),
                section_card(
                    "2. Qual serviço?",
                    rx.grid(
                        rx.foreach(PortalState.servico_opcoes, _cartao_servico),
                        columns=rx.breakpoints(initial="1", sm="2", md="3"),
                        spacing="2",
                        width="100%",
                    ),
                ),
                section_card(
                    "3. Quando?",
                    rx.vstack(
                        rx.hstack(
                            rx.foreach(PortalState.dias, _cartao_dia),
                            spacing="2",
                            overflow_x="auto",
                            width="100%",
                            padding_bottom="0.5rem",
                        ),
                        rx.divider(),
                        rx.cond(
                            PortalState.tem_horario_livre,
                            rx.flex(
                                rx.foreach(PortalState.horarios, _cartao_horario),
                                wrap="wrap",
                                spacing="2",
                                width="100%",
                                padding_top="0.75rem",
                            ),
                            rx.box(
                                rx.text(
                                    "Não há horário livre neste dia. Escolha outro.",
                                    size="2",
                                    color=rx.color("gray", 10),
                                ),
                                padding="1rem 0",
                            ),
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),
                section_card(
                    "4. Algo que devemos saber?",
                    rx.vstack(
                        rx.text_area(
                            placeholder="Sintomas, comportamento, preferências... (opcional)",
                            value=PortalState.ag_observacoes,
                            on_change=PortalState.set_ag_observacoes,
                            width="100%",
                        ),
                        error_banner(PortalState.ag_error),
                        rx.hstack(
                            rx.spacer(),
                            rx.button(
                                rx.cond(
                                    PortalState.ag_enviando,
                                    rx.spinner(size="2"),
                                    rx.icon("calendar-check", size=16),
                                ),
                                "Confirmar consulta",
                                on_click=PortalState.agendar,
                                size="3",
                                disabled=PortalState.ag_enviando
                                | (PortalState.ag_hora == ""),
                            ),
                            width="100%",
                            padding_top="0.5rem",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            rx.card(
                rx.vstack(
                    rx.icon("paw-print", size=28, color=rx.color("gray", 8)),
                    rx.text(
                        "Cadastre um pet antes de marcar a primeira consulta.",
                        color=rx.color("gray", 10),
                    ),
                    rx.link(
                        rx.button(rx.icon("plus", size=16), "Cadastrar pet"),
                        href="/portal/pets",
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                    padding="2rem",
                ),
                width="100%",
            ),
        ),
        title="Marcar consulta",
        subtitle="Escolha o pet, o serviço e o melhor horário.",
    )


# ----------------------------------------------------------------------
# /portal/consultas
# ----------------------------------------------------------------------


def _consulta_card(consulta: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading(consulta["servico"], size="4"),
                    status_badge(consulta["status"], STATUS_AGENDAMENTO_CORES),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.hstack(
                    rx.icon("paw-print", size=14, color=rx.color("gray", 9)),
                    rx.text(consulta["pet"], size="2", color=rx.color("gray", 11)),
                    rx.text("·", color=rx.color("gray", 8)),
                    rx.icon("clock", size=14, color=rx.color("gray", 9)),
                    rx.text(
                        consulta["data_hora"], size="2", color=rx.color("gray", 11)
                    ),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.cond(
                    consulta["observacoes"],
                    rx.text(
                        consulta["observacoes"], size="1", color=rx.color("gray", 10)
                    ),
                ),
                spacing="1",
                align_items="start",
            ),
            rx.spacer(),
            rx.cond(
                consulta["pode_cancelar"],
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button(
                            "Cancelar", variant="soft", color_scheme="red", size="1"
                        )
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Cancelar esta consulta?"),
                        rx.alert_dialog.description(
                            "O horário volta a ficar livre para outras pessoas. "
                            "Para remarcar, será preciso escolher um novo horário."
                        ),
                        rx.hstack(
                            rx.alert_dialog.cancel(
                                rx.button(
                                    "Manter", variant="soft", color_scheme="gray"
                                )
                            ),
                            rx.alert_dialog.action(
                                rx.button(
                                    "Cancelar consulta",
                                    color_scheme="red",
                                    on_click=lambda: PortalState.cancelar_consulta(
                                        consulta["id"]
                                    ),
                                )
                            ),
                            justify="end",
                            spacing="3",
                            padding_top="1rem",
                        ),
                        max_width="28rem",
                    ),
                ),
                rx.fragment(),
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def portal_consultas_page() -> rx.Component:
    return layout_cliente(
        error_banner(PortalState.load_error),
        rx.hstack(
            rx.spacer(),
            rx.link(
                rx.button(rx.icon("plus", size=16), "Marcar consulta"),
                href="/portal/agendar",
            ),
            width="100%",
        ),
        rx.cond(
            PortalState.consultas,
            rx.vstack(
                rx.foreach(PortalState.consultas, _consulta_card),
                spacing="3",
                width="100%",
            ),
            empty_state("Você ainda não tem consultas."),
        ),
        title="Minhas consultas",
        subtitle="O que já passou e o que ainda vem.",
    )


# ----------------------------------------------------------------------
# /portal/historico
# ----------------------------------------------------------------------


def _historico_item(registro: dict) -> rx.Component:
    return rx.hstack(
        # A linha vertical liga um atendimento ao próximo: é o que transforma
        # uma lista de fichas numa história do animal.
        rx.vstack(
            rx.box(
                width="0.7rem",
                height="0.7rem",
                border_radius="50%",
                background=rx.color("jade", 9),
                flex_shrink="0",
            ),
            rx.box(
                width="2px",
                flex_grow="1",
                min_height="1.5rem",
                background=rx.color("gray", 5),
            ),
            spacing="0",
            align="center",
            align_self="stretch",
        ),
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.text(registro["data"], size="2", weight="bold"),
                    rx.badge(registro["pet"], variant="soft", radius="full"),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(
                    "Atendido por ",
                    registro["profissional"],
                    size="1",
                    color=rx.color("gray", 10),
                ),
                rx.divider(margin_y="0.5rem"),
                rx.vstack(
                    rx.text("Diagnóstico", size="1", color=rx.color("gray", 10)),
                    rx.text(registro["diagnostico"], size="2"),
                    spacing="0",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Tratamento", size="1", color=rx.color("gray", 10)),
                    rx.text(registro["tratamento"], size="2"),
                    spacing="0",
                    align_items="start",
                ),
                rx.cond(
                    registro["retorno"] != "-",
                    rx.hstack(
                        rx.icon("calendar-clock", size=14, color=rx.color("jade", 9)),
                        rx.text(
                            "Retorno em ",
                            registro["retorno"],
                            size="1",
                            color=rx.color("jade", 11),
                        ),
                        spacing="1",
                        align="center",
                        padding_top="0.25rem",
                    ),
                ),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            width="100%",
            margin_bottom="0.75rem",
        ),
        spacing="3",
        align="stretch",
        width="100%",
    )


def portal_historico_page() -> rx.Component:
    return layout_cliente(
        error_banner(PortalState.load_error),
        rx.cond(
            PortalState.pet_opcoes,
            rx.hstack(
                rx.select.root(
                    rx.select.trigger(placeholder="Todos os pets"),
                    rx.select.content(
                        rx.select.item("Todos os pets", value=""),
                        rx.foreach(
                            PortalState.pet_opcoes,
                            lambda pet: rx.select.item(
                                pet["nome"], value=pet["id"].to_string()
                            ),
                        ),
                    ),
                    value=PortalState.historico_pet,
                    on_change=PortalState.set_historico_pet,
                ),
                width="100%",
            ),
        ),
        rx.cond(
            PortalState.historico,
            rx.vstack(
                rx.foreach(PortalState.historico, _historico_item),
                spacing="0",
                width="100%",
            ),
            empty_state("Nenhum atendimento registrado ainda."),
        ),
        title="Histórico clínico",
        subtitle="Cada atendimento registrado pela equipe da clínica.",
    )


# ----------------------------------------------------------------------
# /portal/pedidos
# ----------------------------------------------------------------------


def _compra_card(compra: dict) -> rx.Component:
    aberta = PortalState.compra_aberta == compra["id"]
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text("Pedido #", compra["id"], size="2", weight="bold"),
                        status_badge(compra["status"], STATUS_PEDIDO_CORES),
                        spacing="2",
                        align="center",
                    ),
                    rx.text(compra["data"], size="1", color=rx.color("gray", 10)),
                    spacing="1",
                    align_items="start",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("Total", size="1", color=rx.color("gray", 10)),
                    money(compra["total"]),
                    spacing="0",
                    align_items="end",
                ),
                rx.icon_button(
                    rx.cond(
                        aberta,
                        rx.icon("chevron-up", size=16),
                        rx.icon("chevron-down", size=16),
                    ),
                    on_click=lambda: PortalState.abrir_compra(compra["id"]),
                    variant="ghost",
                    color_scheme="gray",
                    size="1",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.cond(
                aberta,
                rx.box(
                    rx.divider(margin_y="0.75rem"),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Produto"),
                                rx.table.column_header_cell("Qtd."),
                                rx.table.column_header_cell("Unitário"),
                                rx.table.column_header_cell("Total"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                PortalState.compra_itens,
                                lambda item: rx.table.row(
                                    rx.table.cell(item["produto"]),
                                    rx.table.cell(item["quantidade"]),
                                    rx.table.cell(money(item["unitario"])),
                                    rx.table.cell(money(item["total"])),
                                ),
                            )
                        ),
                        size="1",
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            spacing="0",
            width="100%",
        ),
        width="100%",
    )


def portal_pedidos_page() -> rx.Component:
    return layout_cliente(
        error_banner(PortalState.load_error),
        rx.cond(
            PortalState.compras,
            rx.vstack(
                rx.foreach(PortalState.compras, _compra_card),
                spacing="3",
                width="100%",
            ),
            empty_state("Você ainda não fez nenhuma compra."),
        ),
        title="Minhas compras",
        subtitle="Os pedidos feitos no petshop.",
    )
