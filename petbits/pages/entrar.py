"""Telas de porta de entrada: entrar e criar conta.

Os dois formulários vivem dentro de `rx.form` para o Enter enviar. Numa tela
de login, obrigar o clique no botão é o tipo de atrito que ninguém reporta
como defeito mas todo mundo sente.
"""

import reflex as rx

from petbits.states.auth_state import AuthState


def _campo(rotulo: str, componente: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(rotulo, size="2", weight="medium"),
        componente,
        spacing="1",
        width="100%",
        align_items="start",
    )


def _casca(
    *campos,
    titulo: str,
    subtitulo: str,
    rotulo_envio: str,
    on_submit,
    rodape: rx.Component,
    aviso: rx.Component | None = None,
) -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.vstack(
                rx.heading(titulo, size="7"),
                rx.text(subtitulo, size="2", color=rx.color("gray", 10)),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            aviso if aviso is not None else rx.fragment(),
            rx.form(
                rx.vstack(
                    *campos,
                    rx.cond(
                        AuthState.erro,
                        rx.callout(
                            AuthState.erro,
                            icon="triangle_alert",
                            color_scheme="red",
                            size="1",
                            width="100%",
                        ),
                    ),
                    rx.button(
                        rotulo_envio,
                        type="submit",
                        size="3",
                        width="100%",
                        disabled=AuthState.enviando,
                        margin_top="0.5rem",
                    ),
                    spacing="3",
                    width="100%",
                ),
                on_submit=on_submit,
                reset_on_submit=False,
                width="100%",
            ),
            rodape,
            spacing="4",
            width="100%",
            max_width="26rem",
            align_items="start",
        ),
        min_height="100vh",
        padding="2rem 1.5rem",
        width="100%",
    )


def entrar_page() -> rx.Component:
    return _casca(
        _campo(
            "E-mail",
            rx.input(
                placeholder="voce@email.com",
                type="email",
                value=AuthState.login_email,
                on_change=AuthState.set_login_email,
                size="3",
                width="100%",
            ),
        ),
        _campo(
            "Senha",
            rx.input(
                placeholder="Sua senha",
                type="password",
                value=AuthState.login_senha,
                on_change=AuthState.set_login_senha,
                size="3",
                width="100%",
            ),
        ),
        titulo="Entrar",
        subtitulo="Acesse sua conta para continuar.",
        rotulo_envio="Entrar",
        on_submit=AuthState.entrar,
        # O aviso de credencial vencida vem antes dos campos: quem foi levado
        # de volta para cá no meio de uma tarefa precisa entender por quê.
        aviso=rx.cond(
            AuthState.sessao_expirou,
            rx.callout(
                "Sua sessão expirou. Entre de novo para continuar.",
                icon="clock",
                color_scheme="amber",
                size="1",
                width="100%",
            ),
        ),
        rodape=rx.hstack(
            rx.text("Ainda não tem conta?", size="2", color=rx.color("gray", 10)),
            rx.link("Cadastre-se", href="/cadastro", size="2", weight="medium"),
            spacing="2",
        ),
    )


def cadastro_page() -> rx.Component:
    return _casca(
        _campo(
            "Nome completo",
            rx.input(
                placeholder="Como podemos te chamar",
                value=AuthState.cad_nome,
                on_change=AuthState.set_cad_nome,
                size="3",
                width="100%",
            ),
        ),
        _campo(
            "E-mail",
            rx.input(
                placeholder="voce@email.com",
                type="email",
                value=AuthState.cad_email,
                on_change=AuthState.set_cad_email,
                size="3",
                width="100%",
            ),
        ),
        _campo(
            "Documento (CPF)",
            rx.input(
                placeholder="000.000.000-00",
                value=AuthState.cad_documento,
                on_change=AuthState.set_cad_documento,
                size="3",
                width="100%",
            ),
        ),
        _campo(
            "Telefone",
            rx.input(
                placeholder="(00) 00000-0000 (opcional)",
                value=AuthState.cad_telefone,
                on_change=AuthState.set_cad_telefone,
                size="3",
                width="100%",
            ),
        ),
        _campo(
            "Endereço",
            rx.input(
                placeholder="Rua, número, bairro (opcional)",
                value=AuthState.cad_endereco,
                on_change=AuthState.set_cad_endereco,
                size="3",
                width="100%",
            ),
        ),
        _campo(
            "Senha",
            rx.input(
                placeholder="Mínimo 8 caracteres",
                type="password",
                value=AuthState.cad_senha,
                on_change=AuthState.set_cad_senha,
                size="3",
                width="100%",
            ),
        ),
        _campo(
            "Confirmar senha",
            rx.input(
                placeholder="Repita a senha",
                type="password",
                value=AuthState.cad_confirmar,
                on_change=AuthState.set_cad_confirmar,
                size="3",
                width="100%",
            ),
        ),
        # A regra aparece antes de o erro acontecer: descobri-la por tentativa
        # e erro é o que faz gente desistir do cadastro.
        rx.text(
            "A senha precisa de pelo menos 8 caracteres, com uma letra e um número.",
            size="1",
            color=rx.color("gray", 10),
        ),
        titulo="Criar conta",
        subtitulo="Cadastre-se para acompanhar os seus pets.",
        rotulo_envio="Criar conta",
        on_submit=AuthState.cadastrar,
        rodape=rx.hstack(
            rx.text("Já tem conta?", size="2", color=rx.color("gray", 10)),
            rx.link("Entrar", href="/entrar", size="2", weight="medium"),
            spacing="2",
        ),
    )
