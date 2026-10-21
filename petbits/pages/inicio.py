"""A casa do tutor: os animais dele.

Deixou de ser um cartão de boas-vindas quando os animais passaram a existir.
O que aparece aqui é o que o backend devolveu — e o backend só devolve os
animais de quem perguntou.
"""

import reflex as rx

from petbits.caminhos import no_site
from petbits import esqueletos
from petbits.pages.historico import dialogo_historico_tutor
from petbits.states.auth_state import AuthState
from petbits.states.historico_state import HistoricoTutorState
from petbits.visual import (LARGURA_DO_CLIENTE, campo, rodape_do_cliente, tela_vazia,
                            titulo_de_pagina, topo_do_cliente)
from petbits.states.pet_state import ID_UPLOAD_ANIMAL, PetState




def _cartao(animal: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.image(src=no_site(rx.cond(animal["foto"], animal["foto"], animal["imagem"])),
                     alt=animal["nome"], width="4.5rem",
                     height="4.5rem", border_radius="1.1rem", flex_shrink="0",
                     object_fit="cover"),
            rx.vstack(
                rx.hstack(
                    rx.heading(animal["nome"], size="4"),
                    rx.badge(animal["especie"], variant="soft", radius="full",
                             color_scheme="orange"),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(animal["raca"], size="2", color=rx.color("gray", 11)),
                rx.hstack(
                    rx.text("Nascimento: ", animal["nascimento"], size="1",
                            color=rx.color("gray", 11)),
                    rx.text("Peso: ", animal["peso"], " kg", size="1",
                            color=rx.color("gray", 11)),
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
            rx.vstack(
                rx.button(
                    "Editar",
                    on_click=lambda: PetState.editar(animal),
                    variant="soft",
                    size="1",
                    width="100%",
                ),
                # A linha do tempo clínica, só de leitura (change `historico-clinico`).
                rx.button(
                    rx.icon("clipboard-list", size=14), "Histórico",
                    on_click=HistoricoTutorState.abrir(animal),
                    variant="soft",
                    color_scheme="gray",
                    size="1",
                    width="100%",
                ),
                spacing="1",
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
                # Foto do animal: o próprio cliente escolhe (change
                # `perfil-e-fotos`, D7). Só depois que o animal existe, porque
                # a foto é gravada pelo id dele.
                rx.cond(
                    PetState.editando_id,
                    rx.hstack(
                        rx.image(src=no_site(rx.cond(PetState.f_foto, PetState.f_foto,
                                                     PetState.f_imagem)),
                                 alt="Foto do animal", width="5.5rem", height="5.5rem",
                                 object_fit="cover", border_radius="1.25rem",
                                 flex_shrink="0"),
                        rx.vstack(
                            rx.upload.root(
                                rx.button(
                                    rx.cond(PetState.enviando_foto, rx.spinner(size="2"),
                                            rx.icon("camera", size=16)),
                                    rx.cond(PetState.f_foto, "Trocar foto",
                                            "Escolher foto"),
                                    variant="soft",
                                    disabled=PetState.enviando_foto,
                                ),
                                id=ID_UPLOAD_ANIMAL,
                                max_files=1,
                                multiple=False,
                                no_drag=True,
                                on_drop=PetState.enviar_foto(
                                    rx.upload_files(upload_id=ID_UPLOAD_ANIMAL)),
                            ),
                            rx.text("JPG, PNG ou WebP, até 5 MB.", size="1",
                                    color=rx.color("gray", 11)),
                            rx.cond(PetState.erro_foto,
                                    rx.text(PetState.erro_foto, size="1",
                                            color=rx.color("red", 11))),
                            spacing="1",
                            align_items="start",
                        ),
                        spacing="3",
                        align="center",
                        width="100%",
                    ),
                    rx.text("Depois de cadastrar, edite o animal para pôr a foto dele.",
                            size="1", color=rx.color("gray", 11)),
                ),
                campo("Nome", rx.input(placeholder="Nome do animal",
                                        value=PetState.f_nome,
                                        on_change=PetState.set_f_nome,
                                        width="100%")),
                rx.hstack(
                    campo("Espécie", rx.input(placeholder="Cão, gato...",
                                               value=PetState.f_especie,
                                               on_change=PetState.set_f_especie,
                                               width="100%")),
                    campo("Raça", rx.input(placeholder="Opcional",
                                            value=PetState.f_raca,
                                            on_change=PetState.set_f_raca,
                                            width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                rx.hstack(
                    campo("Nascimento", rx.input(type="date",
                                                  value=PetState.f_nascimento,
                                                  on_change=PetState.set_f_nascimento,
                                                  width="100%")),
                    campo("Peso (kg)", rx.input(placeholder="Opcional",
                                                 value=PetState.f_peso,
                                                 on_change=PetState.set_f_peso,
                                                 width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                campo("Observações", rx.text_area(
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
        "/fotos/vazio-animais.webp",
        "A casinha ainda está vazia",
        "Cadastre o seu primeiro animal para a clínica poder acompanhá-lo de perto.",
        rx.button(rx.icon("plus", size=16), "Cadastrar animal", on_click=PetState.novo,
                  size="3"),
    )


def _proximo() -> rx.Component:
    """O próximo agendamento (change `proximo-agendamento-na-casa`). Nada
    enquanto a agenda não chega ou se ela falhou (D1)."""
    P = PetState.proximo
    return rx.cond(
        PetState.proximo_carregado,
        rx.card(
            rx.hstack(
                rx.center(rx.icon("calendar-clock", size=22, color=rx.color("teal", 11)),
                          width="2.75rem", height="2.75rem", border_radius="30%",
                          background=rx.color("teal", 3), flex_shrink="0"),
                rx.cond(
                    P.contains("titulo"),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Próximo agendamento", size="1", weight="bold",
                                    color=rx.color("teal", 11)),
                            rx.cond(P["em_andamento"].to(bool),
                                    rx.badge("Em andamento", radius="full", size="1")),
                            spacing="2", align="center",
                        ),
                        rx.text(P["titulo"].to(str), size="3", weight="bold"),
                        rx.text(
                            P["quando"].to(str),
                            rx.cond(P["profissional"].to(str) != "",
                                    rx.text.span(" · com ", P["profissional"].to(str))),
                            size="2",
                            color=rx.color("gray", 11),
                        ),
                        rx.cond(P["outros"].to(str) != "",
                                rx.text("E ", P["outros"].to(str), " depois.", size="1",
                                        color=rx.color("gray", 11))),
                        spacing="1", align_items="start", flex="1",
                    ),
                    rx.vstack(
                        rx.text("Nenhum agendamento marcado", size="3", weight="bold"),
                        rx.text("Consulta, vacina ou banho e tosa: escolha um horário livre.",
                                size="2", color=rx.color("gray", 11)),
                        spacing="1", align_items="start", flex="1",
                    ),
                ),
                rx.link(rx.button(rx.cond(P.contains("titulo"), "Ver na agenda", "Agendar"),
                                  variant="soft", size="2"),
                        href="/agenda"),
                spacing="4", align="center", width="100%", wrap="wrap",
            ),
            width="100%",
        ),
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
            rx.image(src=no_site("/fotos/banner.webp"), alt="Um cão e um gato abraçados",
                     width="17rem", height="11.5rem", object_fit="cover",
                     border_radius="1.25rem", flex_shrink="0",
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
    return esqueletos.cartoes("Carregando os seus animais...", n=2, com_imagem=False)


def inicio_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            topo_do_cliente("/animais"),
            _banner(),
            _proximo(),
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
            dialogo_historico_tutor(),
            rodape_do_cliente(),
            spacing="4", align_items="start", padding_y="2rem", width="100%",
        ),
        size=LARGURA_DO_CLIENTE,
    )
