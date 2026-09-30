"""Cadastro do tutor.

O tutor se cadastra sozinho: esta tela é pública. Ela cria o login e a ficha
de cliente numa requisição só (`POST /cliente/signup`), com `role: "member"`
fixado no backend — quem vira administrador é decidido no painel do Xano,
nunca por um campo de formulário.
"""

import reflex as rx

from petbits.components.auth_layout import auth_layout, campo_senha
from petbits.components.ui import form_field
from petbits.states.auth_state import AuthState


def _campo(rotulo: str, icone: str, placeholder: str, valor, on_change, **kwargs) -> rx.Component:
    return form_field(
        rotulo,
        rx.input(
            rx.input.slot(rx.icon(icone, size=16)),
            placeholder=placeholder,
            value=valor,
            on_change=on_change,
            size="3",
            width="100%",
            **kwargs,
        ),
    )


def cadastro_page() -> rx.Component:
    return auth_layout(
        _campo(
            "Nome completo", "user", "Como podemos te chamar",
            AuthState.cad_nome, AuthState.set_cad_nome,
        ),
        _campo(
            "E-mail", "mail", "voce@email.com",
            AuthState.cad_email, AuthState.set_cad_email, type="email",
        ),
        rx.hstack(
            _campo(
                "CPF", "id-card", "000.000.000-00",
                AuthState.cad_cpf, AuthState.set_cad_cpf,
            ),
            _campo(
                "Telefone", "phone", "(00) 00000-0000",
                AuthState.cad_telefone, AuthState.set_cad_telefone,
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        _campo(
            "Endereço", "map-pin", "Rua, número, bairro",
            AuthState.cad_endereco, AuthState.set_cad_endereco,
        ),
        campo_senha(
            "Senha",
            AuthState.cad_senha,
            AuthState.set_cad_senha,
            AuthState.mostrar_senha,
            AuthState.alternar_senha,
            placeholder="Mínimo 8 caracteres",
        ),
        campo_senha(
            "Confirmar senha",
            AuthState.cad_confirmar,
            AuthState.set_cad_confirmar,
            AuthState.mostrar_senha,
            AuthState.alternar_senha,
            placeholder="Repita a senha",
        ),
        # A regra aparece antes de o erro acontecer: a validação da senha
        # espelha os filtros da coluna no Xano, e descobri-la por tentativa
        # e erro é o que faz gente desistir do cadastro.
        rx.text(
            "A senha precisa de pelo menos 8 caracteres, com uma letra e um número.",
            size="1",
            color=rx.color("gray", 10),
        ),
        titulo="Criar conta",
        subtitulo="Cadastre-se para acompanhar os seus pets.",
        erro=AuthState.auth_error,
        enviando=AuthState.enviando,
        rotulo_envio="Criar conta",
        on_submit=AuthState.cadastrar,
        rodape=rx.hstack(
            rx.text("Já tem conta?", size="2", color=rx.color("gray", 10)),
            rx.link("Entrar", href="/login", size="2", weight="medium"),
            spacing="2",
            width="100%",
        ),
    )
