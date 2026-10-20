"""Meu perfil: dados, foto e senha — do tutor e de quem é da equipe.

O do tutor veio na change `perfil-e-fotos`: CPF e e-mail aparecem travados,
porque o CPF identifica a pessoa e o e-mail é o login. O da equipe veio na
`perfil-do-colaborador`: função, e-mail e data de entrada travados, porque
quem os define é a gerência. Os blocos são os mesmos para os dois; cada um
recebe o seu State.
"""

import reflex as rx

from petbits import esqueletos
from petbits.pages.equipe import _casca
from petbits.states.perfil_state import (ID_UPLOAD, ID_UPLOAD_EQUIPE, PerfilEquipeState,
                                         PerfilState)
from petbits.visual import LARGURA_DO_CLIENTE, campo, titulo_de_pagina, topo_do_cliente




def _travado(rotulo: str, valor) -> rx.Component:
    return campo(rotulo, rx.input(value=valor, disabled=True, width="100%", size="3"))


def _aviso(texto, cor: str, icone: str) -> rx.Component:
    return rx.cond(texto, rx.callout(texto, icon=icone, color_scheme=cor, size="1",
                                     width="100%"))


def _foto(S, id_upload: str, legenda=None) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.avatar(src=S.foto_url, fallback=S.iniciais,
                      radius="full", size="8", color_scheme="teal", variant="solid",
                      custom_attrs={"alt": "Sua foto de perfil"}),
            rx.heading(S.nome, size="5", text_align="center"),
            legenda if legenda is not None else rx.fragment(),
            rx.text(S.email, size="2", color=rx.color("gray", 11)),
            rx.upload.root(
                rx.button(
                    rx.cond(S.enviando_foto, rx.spinner(size="2"), rx.icon("camera", size=16)),
                    rx.cond(S.foto_url, "Trocar foto", "Enviar foto"),
                    variant="soft",
                    disabled=S.enviando_foto,
                ),
                id=id_upload,
                max_files=1,
                multiple=False,
                no_drag=True,
                on_drop=S.enviar_foto(rx.upload_files(upload_id=id_upload)),
            ),
            rx.text("JPG, PNG ou WebP, até 5 MB.", size="1", color=rx.color("gray", 11)),
            _aviso(S.erro_foto, "red", "triangle_alert"),
            spacing="3",
            align="center",
            width="100%",
            padding="1rem",
        ),
        width="100%",
    )


def _dados(S, *meio: rx.Component, nota: str) -> rx.Component:
    """Nome no topo, os campos da área no meio, e o salvar."""
    return rx.card(
        rx.vstack(
            rx.heading("Seus dados", size="4"),
            campo("Nome", rx.input(value=S.nome, on_change=S.set_nome, width="100%",
                                    size="3")),
            *meio,
            rx.text(nota, size="1", color=rx.color("gray", 11)),
            _aviso(S.erro_dados, "red", "triangle_alert"),
            rx.button("Salvar dados", on_click=S.salvar_dados, disabled=S.salvando, size="3"),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def _telefone(S) -> rx.Component:
    return campo("Telefone", rx.input(value=S.telefone, on_change=S.set_telefone,
                                       placeholder="(00) 00000-0000", width="100%", size="3"))


def _em_duas(*filhos: rx.Component) -> rx.Component:
    return rx.grid(*filhos, columns=rx.breakpoints(initial="1", sm="2"), spacing="3",
                   width="100%")


def _senha(S) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Trocar senha", size="4"),
            campo("Senha atual", rx.input(type="password", value=S.senha_atual,
                                           on_change=S.set_senha_atual, width="100%",
                                           size="3")),
            _em_duas(
                campo("Nova senha", rx.input(type="password", value=S.nova_senha,
                                              on_change=S.set_nova_senha, width="100%",
                                              size="3")),
                campo("Repita a nova", rx.input(type="password", value=S.confirmar,
                                                 on_change=S.set_confirmar, width="100%",
                                                 size="3")),
            ),
            rx.text("Pelo menos 8 caracteres, com uma letra e um número.", size="1",
                    color=rx.color("gray", 11)),
            _aviso(S.erro_senha, "red", "triangle_alert"),
            rx.button("Trocar senha", on_click=S.trocar_senha, disabled=S.trocando,
                      variant="soft", size="3"),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def _carregado(S, conteudo: rx.Component) -> rx.Component:
    return rx.cond(
        S.ja_carregou & ~S.erro.bool(),
        conteudo,
        # Sem dado e sem erro é carga (change `esqueletos-de-carregamento`).
        rx.cond(~S.erro.bool(), esqueletos.perfil("Carregando o perfil...")),
    )


def _grade(*filhos: rx.Component) -> rx.Component:
    return rx.grid(*filhos, columns=rx.breakpoints(initial="1", md="1fr 2fr"), spacing="4",
                   width="100%", align_items="start")


def perfil_page() -> rx.Component:
    S = PerfilState
    return rx.container(
        rx.vstack(
            topo_do_cliente("/perfil"),
            titulo_de_pagina("Meu perfil", "Seus dados, sua foto e sua senha."),
            _aviso(S.erro, "red", "triangle_alert"),
            _carregado(S, _grade(
                _foto(S, ID_UPLOAD),
                rx.vstack(
                    _dados(
                        S,
                        _em_duas(_telefone(S), _travado("CPF", S.documento)),
                        campo("Endereço", rx.input(value=S.endereco,
                                                    on_change=S.set_endereco,
                                                    placeholder="Rua, número, bairro",
                                                    width="100%", size="3")),
                        _travado("E-mail", S.email),
                        nota="CPF e e-mail só a clínica altera.",
                    ),
                    _senha(S),
                    spacing="4",
                    width="100%",
                ),
            )),
            spacing="4",
            align_items="start",
            padding_y="2rem",
            width="100%",
        ),
        size=LARGURA_DO_CLIENTE,
    )


def perfil_equipe_page() -> rx.Component:
    """O mesmo perfil, na casca da clínica (change `perfil-do-colaborador`)."""
    S = PerfilEquipeState
    sem_ficha = rx.callout(
        "Não há uma ficha de colaborador com o seu e-mail, então seus dados e sua foto "
        "ficam com a gerência. A troca de senha funciona normalmente.",
        icon="info",
        color_scheme="amber",
        size="1",
        width="100%",
    )
    return _casca(
        _aviso(S.erro, "red", "triangle_alert"),
        _carregado(S, rx.cond(
            S.tem_ficha,
            _grade(
                _foto(S, ID_UPLOAD_EQUIPE,
                      legenda=rx.cond(S.funcao, rx.badge(S.funcao, variant="soft",
                                                         color_scheme="orange",
                                                         radius="full"))),
                rx.vstack(
                    _dados(
                        S,
                        _em_duas(_telefone(S), _travado("Função", S.funcao)),
                        _em_duas(_travado("E-mail", S.email),
                                 _travado("Na clínica desde", S.data_entrada)),
                        nota="Função, e-mail e data de entrada só a gerência altera.",
                    ),
                    _senha(S),
                    spacing="4",
                    width="100%",
                ),
            ),
            rx.vstack(sem_ficha, _senha(S), spacing="4", width="100%", max_width="40rem"),
        )),
        rota="/equipe/perfil",
        titulo="Meu perfil",
        subtitulo="Seus dados, sua foto e sua senha.",
    )
