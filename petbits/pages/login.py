"""Tela de entrada."""

import reflex as rx

from petbits.components.auth_layout import auth_layout, campo_senha
from petbits.components.ui import form_field
from petbits.states.auth_state import AuthState


def login_page() -> rx.Component:
    return auth_layout(
        # O aviso de sessão vencida vem antes dos campos: quem foi expulso no
        # meio de uma tarefa precisa entender por que voltou para cá.
        rx.cond(
            AuthState.sessao_expirou,
            rx.callout(
                "Sua sessão expirou. Entre de novo para continuar.",
                icon="clock",
                color_scheme="amber",
                size="1",
                width="100%",
            ),
        ),
        form_field(
            "E-mail",
            rx.input(
                rx.input.slot(rx.icon("mail", size=16)),
                placeholder="voce@email.com",
                type="email",
                value=AuthState.login_email,
                on_change=AuthState.set_login_email,
                size="3",
                width="100%",
            ),
        ),
        campo_senha(
            "Senha",
            AuthState.login_senha,
            AuthState.set_login_senha,
            AuthState.mostrar_senha,
            AuthState.alternar_senha,
        ),
        titulo="Entrar",
        subtitulo="Acesse sua conta para continuar.",
        erro=AuthState.auth_error,
        enviando=AuthState.enviando,
        rotulo_envio="Entrar",
        on_submit=AuthState.entrar,
        rodape=rx.hstack(
            rx.text("Ainda não tem conta?", size="2", color=rx.color("gray", 10)),
            rx.link("Cadastre-se", href="/cadastro", size="2", weight="medium"),
            spacing="2",
            width="100%",
        ),
    )
