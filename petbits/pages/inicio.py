"""A casa do tutor: os animais dele.

Deixou de ser um cartão de boas-vindas quando os animais passaram a existir.
O que aparece aqui é o que o backend devolveu — e o backend só devolve os
animais de quem perguntou.
"""

import reflex as rx

from petbits.states.auth_state import AuthState
from petbits.visual import tela_vazia, titulo_de_pagina, topo_do_cliente
from petbits.states.pet_state import PetState


def _campo(rotulo: str, componente: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(rotulo, size="2", weight="medium"),
        componente,
        spacing="1",
        width="100%",
        align_items="start",
    )


def _cartao(animal: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.image(src=animal["imagem"], alt=animal["especie"], width="4.5rem",
                     height="4.5rem", border_radius="1.1rem", flex_shrink="0"),
            rx.vstack(
                rx.hstack(
                    rx.heading(animal["nome"], size="4"),
                    rx.badge(animal["especie"], variant="soft", radius="full",
                             color_scheme="orange"),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(animal["raca"], size="2", color=rx.color("gray", 10)),
                rx.hstack(
                    rx.text("Nascimento: ", animal["nascimento"], size="1",
                            color=rx.color("gray", 10)),
                    rx.text("Peso: ", animal["peso"], " kg", size="1",
                            color=rx.color("gray", 10)),
                    spacing="4",
                    wrap="wrap",
                ),
                rx.cond(
                    animal["observacoes"],
                    rx.text(animal["observacoes"], size="1",
                            color=rx.color("gray", 11), padding_top="0.25rem"),
                ),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            rx.spacer(),
            rx.button(
                "Editar",
                on_click=lambda: PetState.editar(animal),
                variant="soft",
                size="1",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def _dialogo() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(PetState.titulo_dialogo),
            rx.vstack(
                _campo("Nome", rx.input(placeholder="Nome do animal",
                                        value=PetState.f_nome,
                                        on_change=PetState.set_f_nome,
                                        width="100%")),
                rx.hstack(
                    _campo("Espécie", rx.input(placeholder="Cão, gato...",
                                               value=PetState.f_especie,
                                               on_change=PetState.set_f_especie,
                                               width="100%")),
                    _campo("Raça", rx.input(placeholder="Opcional",
                                            value=PetState.f_raca,
                                            on_change=PetState.set_f_raca,
                                            width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                rx.hstack(
                    _campo("Nascimento", rx.input(type="date",
                                                  value=PetState.f_nascimento,
                                                  on_change=PetState.set_f_nascimento,
                                                  width="100%")),
                    _campo("Peso (kg)", rx.input(placeholder="Opcional",
                                                 value=PetState.f_peso,
                                                 on_change=PetState.set_f_peso,
                                                 width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                _campo("Observações", rx.text_area(
                    placeholder="Alergias, cuidados especiais...",
                    value=PetState.f_observacoes,
                    on_change=PetState.set_f_observacoes,
                    width="100%")),
                rx.cond(
                    PetState.form_error,
                    rx.callout(PetState.form_error, icon="triangle_alert",
                               color_scheme="red", size="1", width="100%"),
                ),
                rx.hstack(
                    rx.button("Cancelar", on_click=PetState.fechar,
                              variant="soft", color_scheme="gray"),
                    rx.button("Salvar", on_click=PetState.salvar,
                              disabled=PetState.salvando),
                    justify="end", spacing="3", width="100%",
                    padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="34rem",
        ),
        open=PetState.show_dialog,
        on_open_change=PetState.set_show_dialog,
    )


def _vazio() -> rx.Component:
    return tela_vazia(
        "/ilustracoes/vazio-animais.svg",
        "A casinha ainda está vazia",
        "Cadastre o seu primeiro animal para a clínica poder acompanhá-lo de perto.",
        rx.button(rx.icon("plus", size=16), "Cadastrar animal", on_click=PetState.novo,
                  size="3"),
    )


def _banner() -> rx.Component:
    """Boas-vindas da casa (D3): saudação, atalhos e a ilustração."""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.badge("PetBits · clínica e petshop", variant="soft",
                         color_scheme="orange", radius="full"),
                rx.heading("Olá, ", AuthState.primeiro_nome, "!", size="8",
                           weight="bold"),
                rx.text("Que bom ter você e os seus por aqui. Marque um atendimento "
                        "ou passe na lojinha.", size="3", color=rx.color("gray", 11),
                        max_width="28rem"),
                rx.hstack(
                    rx.link(rx.button(rx.icon("calendar", size=16), "Agendar", size="3"),
                            href="/agenda"),
                    rx.link(rx.button(rx.icon("shopping-bag", size=16), "Ir à loja",
                                      size="3", variant="soft"),
                            href="/loja"),
                    spacing="3",
                    wrap="wrap",
                    padding_top="0.5rem",
                ),
                spacing="2",
                align_items="start",
                flex="1",
            ),
            rx.image(src="/ilustracoes/banner.svg", alt="", width="17rem",
                     height="auto", flex_shrink="0",
                     display=rx.breakpoints(initial="none", sm="block")),
            align="center",
            spacing="4",
            width="100%",
        ),
        size="4",
        width="100%",
        background=f"linear-gradient(120deg, {rx.color('teal', 3)}, {rx.color('orange', 2)})",
    )


def _carregando() -> rx.Component:
    """Enquanto a lista não chegou, não dizer que ela está vazia."""
    return rx.center(
        rx.hstack(
            rx.spinner(size="2"),
            rx.text("Carregando os seus animais...", size="2",
                    color=rx.color("gray", 10)),
            spacing="2", align="center",
        ),
        padding="3rem", width="100%",
    )


def inicio_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            topo_do_cliente("/"),
            _banner(),
            rx.hstack(
                titulo_de_pagina("Seus animais", "Os seus animais sob cuidado da clínica."),
                rx.spacer(),
                # Agendar, Loja e Meus pedidos saíram daqui: estão no cabeçalho
                # (change `identidade-visual`, D4).
                rx.cond(
                    PetState.tem_animais,
                    rx.button(rx.icon("plus", size=16), "Novo animal",
                              on_click=PetState.novo),
                    rx.fragment(),
                ),
                width="100%", align="center",
            ),
            # Conta cujo papel não é nem equipe nem tutor. Acontece de
            # verdade: `role` é coluna opcional e as contas de equipe nascem
            # à mão no painel do Xano. Antes desta change a pessoa caía aqui
            # e lia "Nenhum animal cadastrado ainda", que é absurdo — ela não
            # tem animais porque não é tutora, não porque não cadastrou.
            #
            # O aviso não vaza nada: só é visto por quem já tem a senha da
            # própria conta.
            rx.cond(
                AuthState.papel_indefinido,
                rx.callout(
                    "Sua conta está sem perfil definido. Procure a clínica para "
                    "liberar o seu acesso.",
                    icon="circle_alert",
                    color_scheme="amber",
                    size="1",
                    width="100%",
                ),
            ),
            # Atalho para quem é da equipe e caiu aqui por digitar o endereço.
            rx.cond(
                AuthState.eh_equipe,
                # Texto e link soltos: o callout põe os filhos num <p>, e um
                # hstack ali dentro é <div> em <p> (change `cliente-ilustrado`, D5).
                rx.callout(
                    rx.fragment(
                        "Você tem acesso à área da clínica. ",
                        rx.link("Abrir o painel", href="/equipe", weight="medium"),
                    ),
                    icon="info",
                    size="1",
                    width="100%",
                ),
            ),
            rx.cond(
                PetState.load_error,
                rx.callout(PetState.load_error, icon="triangle_alert",
                           color_scheme="red", size="1", width="100%"),
            ),
            rx.cond(
                PetState.tem_animais,
                rx.grid(
                    rx.foreach(PetState.animais, _cartao),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="3", width="100%",
                ),
                # QUATRO estados disjuntos: tem, está vindo, está vazio, e
                # falhou. O quarto é o que se esquece — com "carregando" como
                # caso padrão, a tela mostrava o erro e o spinner juntos. O
                # erro já aparece no callout acima, então aqui não vai nada.
                rx.cond(
                    PetState.mostrar_carregando,
                    _carregando(),
                    rx.cond(PetState.mostrar_vazio, _vazio(), rx.fragment()),
                ),
            ),
            _dialogo(),
            spacing="4", align_items="start", padding_y="2rem", width="100%",
        ),
        size="3",
    )
