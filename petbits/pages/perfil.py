"""Meu perfil: dados de contato, foto e senha (change `perfil-e-fotos`).

CPF e e-mail aparecem travados: o CPF identifica a pessoa e o e-mail é o
login, e os dois continuam pela clínica.
"""

import reflex as rx

from petbits.states.perfil_state import ID_UPLOAD, PerfilState
from petbits.visual import titulo_de_pagina, topo_do_cliente


def _campo(rotulo: str, componente: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(rotulo, size="2", weight="medium"),
        componente,
        spacing="1",
        width="100%",
        align_items="start",
    )


def _aviso(texto, cor: str, icone: str) -> rx.Component:
    return rx.cond(texto, rx.callout(texto, icon=icone, color_scheme=cor, size="1",
                                     width="100%"))


def _foto() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.avatar(src=PerfilState.foto_url, fallback=PerfilState.iniciais,
                      radius="full", size="8", color_scheme="teal", variant="solid"),
            rx.heading(PerfilState.nome, size="5", text_align="center"),
            rx.text(PerfilState.email, size="2", color=rx.color("gray", 10)),
            rx.upload.root(
                rx.button(
                    rx.cond(PerfilState.enviando_foto, rx.spinner(size="2"),
                            rx.icon("camera", size=16)),
                    rx.cond(PerfilState.foto_url, "Trocar foto", "Enviar foto"),
                    variant="soft",
                    disabled=PerfilState.enviando_foto,
                ),
                id=ID_UPLOAD,
                max_files=1,
                multiple=False,
                no_drag=True,
                on_drop=PerfilState.enviar_foto(rx.upload_files(upload_id=ID_UPLOAD)),
            ),
            rx.text("JPG, PNG ou WebP, até 5 MB.", size="1", color=rx.color("gray", 10)),
            _aviso(PerfilState.erro_foto, "red", "triangle_alert"),
            spacing="3",
            align="center",
            width="100%",
            padding="1rem",
        ),
        width="100%",
    )


def _dados() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Seus dados", size="4"),
            _campo("Nome", rx.input(value=PerfilState.nome, on_change=PerfilState.set_nome,
                                    width="100%", size="3")),
            rx.grid(
                _campo("Telefone", rx.input(value=PerfilState.telefone,
                                            on_change=PerfilState.set_telefone,
                                            placeholder="(00) 00000-0000", width="100%",
                                            size="3")),
                _campo("CPF", rx.input(value=PerfilState.documento, disabled=True,
                                       width="100%", size="3")),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="3",
                width="100%",
            ),
            _campo("Endereço", rx.input(value=PerfilState.endereco,
                                        on_change=PerfilState.set_endereco,
                                        placeholder="Rua, número, bairro", width="100%",
                                        size="3")),
            _campo("E-mail", rx.input(value=PerfilState.email, disabled=True, width="100%",
                                      size="3")),
            rx.text("CPF e e-mail só a clínica altera.", size="1",
                    color=rx.color("gray", 10)),
            _aviso(PerfilState.erro_dados, "red", "triangle_alert"),
            _aviso(PerfilState.aviso_dados, "green", "circle_check"),
            rx.button("Salvar dados", on_click=PerfilState.salvar_dados,
                      disabled=PerfilState.salvando, size="3"),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def _senha() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Trocar senha", size="4"),
            _campo("Senha atual", rx.input(type="password", value=PerfilState.senha_atual,
                                           on_change=PerfilState.set_senha_atual,
                                           width="100%", size="3")),
            rx.grid(
                _campo("Nova senha", rx.input(type="password", value=PerfilState.nova_senha,
                                              on_change=PerfilState.set_nova_senha,
                                              width="100%", size="3")),
                _campo("Repita a nova", rx.input(type="password",
                                                 value=PerfilState.confirmar,
                                                 on_change=PerfilState.set_confirmar,
                                                 width="100%", size="3")),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="3",
                width="100%",
            ),
            rx.text("Pelo menos 8 caracteres, com uma letra e um número.", size="1",
                    color=rx.color("gray", 10)),
            _aviso(PerfilState.erro_senha, "red", "triangle_alert"),
            _aviso(PerfilState.aviso_senha, "green", "circle_check"),
            rx.button("Trocar senha", on_click=PerfilState.trocar_senha,
                      disabled=PerfilState.trocando, variant="soft", size="3"),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def perfil_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            topo_do_cliente("/perfil"),
            titulo_de_pagina("Meu perfil", "Seus dados, sua foto e sua senha."),
            _aviso(PerfilState.erro, "red", "triangle_alert"),
            rx.cond(
                PerfilState.ja_carregou & ~PerfilState.erro.bool(),
                rx.grid(
                    _foto(),
                    rx.vstack(_dados(), _senha(), spacing="4", width="100%"),
                    columns=rx.breakpoints(initial="1", md="1fr 2fr"),
                    spacing="4",
                    width="100%",
                    align_items="start",
                ),
                rx.cond(PerfilState.carregando,
                        rx.hstack(rx.spinner(size="2"), rx.text("Carregando o perfil..."),
                                  spacing="2")),
            ),
            spacing="4",
            align_items="start",
            padding_y="2rem",
            width="100%",
        ),
        size="3",
    )
