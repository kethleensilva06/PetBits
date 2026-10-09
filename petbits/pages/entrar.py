"""Telas de porta de entrada: entrar e criar conta.

Os dois formulários vivem dentro de `rx.form` para o Enter enviar. Numa tela
de login, obrigar o clique no botão é o tipo de atrito que ninguém reporta
como defeito mas todo mundo sente.
"""

import reflex as rx
from reflex.utils.exec import is_prod_mode

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


def _abas() -> rx.Component:
    """Cliente e Colaborador.

    As duas abas são **o mesmo formulário e o mesmo manipulador de estado**,
    não dois. Isso não é economia de código: é o que faz o número de
    requisições e o tempo de resposta serem iguais nas duas **por
    construção**, e não por cuidado de quem revisa.

    A aba não é enviada ao servidor — nem no corpo, nem na query, nem em
    cabeçalho, nem no caminho. Enquanto o backend não souber qual aba foi
    usada, nenhuma mudança futura consegue fazer a resposta depender dela.

    Se as duas verificassem de jeitos diferentes, descobrir quem é
    colaborador da clínica seria tentar o mesmo e-mail nas duas e ver em qual
    passa — e isso entrega o organograma a qualquer pessoa.

    **Quem entrar pela aba "errada" com a senha certa entra em silêncio**, e
    vai para a área do papel da conta. Um aviso de "esta conta não é da
    equipe" seria a única diferença observável entre as abas, e seria o
    oráculo inteiro de volta.
    """
    return rx.segmented_control.root(
        rx.segmented_control.item("Cliente", value="cliente"),
        rx.segmented_control.item("Colaborador", value="colaborador"),
        value=AuthState.aba,
        on_change=AuthState.set_aba,
        width="100%",
    )


def _conta_teste(conta: rx.Var, indice: rx.Var) -> rx.Component:
    return rx.button(
        rx.text(conta["email"], size="2", weight="medium", trim="both"),
        rx.spacer(),
        rx.text(conta["rotulo"], size="1", color=rx.color("gray", 10), trim="both"),
        on_click=AuthState.escolher_conta_teste(indice),
        variant="ghost",
        color_scheme="gray",
        width="100%",
        justify="between",
        padding="0.4rem 0.5rem",
        margin="0",
        cursor="pointer",
    )


def _painel_contas_teste() -> rx.Component:
    """A janelinha do `Alt+1`, igual à do projeto Mercadinho.

    Só é montada fora de produção (`entrar_page`), e os manipuladores recusam
    em produção mesmo assim. A lista é a mesma nas duas abas.
    """
    return rx.fragment(
        rx.window_event_listener(on_key_down=AuthState.tecla_na_entrada),
        rx.cond(
            AuthState.painel_teste_aberto,
            rx.box(
                rx.hstack(
                    rx.text(
                        AuthState.titulo_painel_teste,
                        size="1",
                        weight="bold",
                        color=rx.color("gray", 10),
                    ),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x", size=14),
                        on_click=AuthState.fechar_painel_teste,
                        variant="ghost",
                        color_scheme="gray",
                        size="1",
                        aria_label="Fechar",
                    ),
                    align="center",
                    width="100%",
                    margin_bottom="0.25rem",
                ),
                rx.cond(
                    AuthState.contas_teste.length() > 0,
                    rx.vstack(
                        rx.foreach(AuthState.contas_teste, _conta_teste),
                        spacing="1",
                        width="100%",
                    ),
                    rx.text(
                        "Nenhuma conta com senha neste grupo. Preencha a senha "
                        "em contas-de-teste.local.txt (veja o README).",
                        size="1",
                        color=rx.color("gray", 10),
                    ),
                ),
                position="fixed",
                left="1rem",
                bottom="1rem",
                width="20rem",
                max_width="calc(100vw - 2rem)",
                padding="0.75rem",
                border_radius="12px",
                background=rx.color("gray", 1),
                border=f"1px solid {rx.color('gray', 6)}",
                box_shadow="0 8px 24px rgba(0, 0, 0, 0.15)",
                z_index="10",
            ),
        ),
    )


def entrar_page() -> rx.Component:
    pagina = _formulario_de_entrada()
    if is_prod_mode():
        return pagina
    return rx.fragment(pagina, _painel_contas_teste())


def _formulario_de_entrada() -> rx.Component:
    return _casca(
        _abas(),
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
        subtitulo="Clientes e equipe da clínica entram por aqui.",
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
        # O rodapé é IGUAL nas duas abas, de propósito. Esconder o
        # "Cadastre-se" na aba Colaborador pareceria arrumação e seria uma
        # diferença observável entre as abas antes de qualquer requisição
        # sair — o formulário viraria o oráculo sozinho.
        rodape=rx.vstack(
            rx.hstack(
                rx.text("Ainda não tem conta?", size="2", color=rx.color("gray", 10)),
                rx.link("Cadastre-se", href="/cadastro", size="2", weight="medium"),
                spacing="2",
            ),
            rx.text(
                "Colaboradores recebem o acesso da clínica.",
                size="1",
                color=rx.color("gray", 9),
            ),
            spacing="1",
            align_items="start",
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
