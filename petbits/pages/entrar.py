"""Telas de porta de entrada: entrar e criar conta.

Os dois formulários vivem dentro de `rx.form` para o Enter enviar. Numa tela
de login, obrigar o clique no botão é o tipo de atrito que ninguém reporta
como defeito mas todo mundo sente.
"""

import reflex as rx
from reflex.utils.exec import is_prod_mode

from petbits.caminhos import no_site
from petbits.states.auth_state import AuthState
from petbits.visual import campo, horario_e_contato, marca


def _campo_senha(
    rotulo: str, placeholder: str, valor, on_change, tipo, icone, alternar
) -> rx.Component:
    """Campo de senha com o olho de conferir o que foi digitado.

    Numa tela onde a recusa é genérica de propósito — "credenciais
    inválidas", sem dizer o quê —, errar a senha e não poder conferir o que
    foi digitado é atrito gratuito.

    O botão fica **fora** da ordem de tabulação (`tab_index=-1`): quem navega
    pelo teclado vai do campo direto para o Entrar, como antes. E ele não é
    `type="submit"`, senão clicar no olho enviaria o formulário.
    """
    return campo(
        rotulo,
        rx.hstack(
            rx.input(
                placeholder=placeholder,
                type=tipo,
                value=valor,
                on_change=on_change,
                size="3",
                width="100%",
            ),
            rx.icon_button(
                rx.icon(icone, size=18),
                on_click=alternar,
                type="button",
                tab_index=-1,
                variant="soft",
                color_scheme="gray",
                size="3",
                aria_label="Mostrar ou ocultar a senha",
            ),
            spacing="2",
            width="100%",
            align="center",
        ),
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
            marca("/boas-vindas"),
            rx.card(
                rx.vstack(
                    rx.vstack(
                        rx.heading(titulo, size="7", weight="bold"),
                        rx.text(subtitulo, size="2", color=rx.color("gray", 11)),
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
                    align_items="start",
                ),
                size="4",
                width="100%",
            ),
            spacing="5",
            width="100%",
            max_width="28rem",
            align_items="center",
        ),
        min_height="100vh",
        padding="2rem 1.5rem",
        width="100%",
    )


def _conta_teste(conta: rx.Var, indice: rx.Var) -> rx.Component:
    return rx.button(
        rx.text(conta["email"], size="2", weight="medium", trim="both"),
        rx.spacer(),
        rx.text(conta["rotulo"], size="1", color=rx.color("gray", 11), trim="both"),
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
    em produção mesmo assim. A lista é a mesma nas duas entradas.
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
                        color=rx.color("gray", 11),
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
                        color=rx.color("gray", 11),
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


def _com_atalhos(pagina: rx.Component) -> rx.Component:
    """Os atalhos Alt+1/Alt+2 só existem fora de produção."""
    if is_prod_mode():
        return pagina
    return rx.fragment(pagina, _painel_contas_teste())


def entrar_page() -> rx.Component:
    """Entrada de clientes (change `porta-de-entrada`)."""
    return _com_atalhos(
        _formulario_de_entrada(
            titulo="Entrar",
            subtitulo="Área do cliente: seus animais e seus agendamentos.",
            rodape=rx.vstack(
                rx.hstack(
                    rx.text("Ainda não tem conta?", size="2", color=rx.color("gray", 11)),
                    rx.link("Cadastre-se", href="/cadastro", size="2", weight="medium"),
                    spacing="2",
                ),
                rx.hstack(
                    rx.text("É da equipe?", size="2", color=rx.color("gray", 11)),
                    rx.link("Entrada da equipe", href="/entrar/equipe", size="2",
                            weight="medium"),
                    spacing="2",
                ),
                spacing="1",
                align_items="start",
            ),
        )
    )


def entrar_equipe_page() -> rx.Component:
    """Entrada da equipe (change `porta-de-entrada`).

    Sem "Cadastre-se" (D2): contas de equipe são dadas pela clínica. É uma
    diferença entre PÁGINAS, fixa para qualquer conta — não diz nada sobre o
    e-mail digitado.
    """
    return _com_atalhos(
        _formulario_de_entrada(
            titulo="Entrada da equipe",
            subtitulo="Gerência da clínica: agenda, colaboradores, serviços e clientes.",
            rodape=rx.vstack(
                rx.text("O acesso da equipe é liberado pela clínica.", size="2",
                        color=rx.color("gray", 11)),
                rx.hstack(
                    rx.text("É cliente?", size="2", color=rx.color("gray", 11)),
                    rx.link("Entrada de clientes", href="/entrar", size="2",
                            weight="medium"),
                    spacing="2",
                ),
                spacing="1",
                align_items="start",
            ),
        )
    )


def _caminho(icone: str, titulo: str, texto: str, rotulo: str, href: str,
             variante: str = "solid") -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(rx.icon(icone, size=24, color=rx.color("teal", 11)),
                      width="3rem", height="3rem", border_radius="30%",
                      background=rx.color("teal", 3)),
            rx.heading(titulo, size="4", weight="bold", padding_top="0.25rem"),
            rx.text(texto, size="2", color=rx.color("gray", 11)),
            rx.spacer(),
            rx.link(rx.button(rotulo, variant=variante, size="3", width="100%"),
                    href=href, width="100%"),
            spacing="2",
            align_items="start",
            height="100%",
        ),
        size="3",
        width="100%",
    )


# As fotos da página inicial (change `boas-vindas-com-fotos`, D1): todas já
# acompanham o app e têm crédito em `assets/fotos/CREDITOS.md`.
FOTO_DA_CAPA = ("/fotos/banner.webp", "Um cão e um gato deitados juntos na grama")
SERVICOS_DA_CLINICA = (
    ("/fotos/vazio-agenda.webp", "Um chihuahua no colo da veterinária, em consulta",
     "stethoscope", "Clínica",
     "Consultas, vacinas e o histórico de cada atendimento, que você acompanha pelo site."),
    ("/fotos/produto-higiene.webp", "Um cão na banheira, ao lado de um xampu",
     "bath", "Banho e tosa",
     "Marque o horário pelo site e veja os horários livres de cada dia."),
    ("/fotos/vazio-pedidos.webp", "Um dachshund dentro de uma caixa de papelão",
     "shopping-bag", "Petshop",
     "Ração, petiscos, brinquedos e higiene, para retirar na clínica ou receber em casa."),
)


def _capa() -> rx.Component:
    """Texto e atalhos à esquerda, a foto à direita; no celular a foto vem
    primeiro, mais baixa (D3)."""
    texto = rx.vstack(
        marca(tamanho="7"),
        rx.heading("Cuidado de verdade para quem faz parte da família", size="8",
                   weight="bold", line_height="1.15"),
        rx.text(
            "Clínica veterinária e petshop. Acompanhe seus animais, marque consultas e "
            "banho e tosa, e compre o que eles precisam.",
            size="4",
            color=rx.color("gray", 11),
        ),
        rx.hstack(
            rx.link(rx.button(rx.icon("log-in", size=16), "Entrar", size="3"),
                    href="/entrar"),
            rx.link(rx.button(rx.icon("user-plus", size=16), "Criar conta", size="3",
                              variant="outline"),
                    href="/cadastro"),
            spacing="3",
            wrap="wrap",
        ),
        spacing="4",
        align_items="start",
        justify="center",
        height="100%",
    )
    foto = rx.image(
        src=no_site(FOTO_DA_CAPA[0]),
        alt=FOTO_DA_CAPA[1],
        width="100%",
        height=rx.breakpoints(initial="13rem", md="24rem"),
        object_fit="cover",
        border_radius="1.5rem",
        box_shadow=f"0 18px 40px -20px {rx.color('teal', 9)}",
    )
    return rx.grid(
        rx.box(texto, order=rx.breakpoints(initial="2", md="1")),
        rx.box(foto, order=rx.breakpoints(initial="1", md="2")),
        columns=rx.breakpoints(initial="1", md="1.1fr 1fr"),
        spacing="6",
        width="100%",
        align_items="center",
    )


def _servico(foto: str, alt: str, icone: str, titulo: str, texto: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.image(src=no_site(foto), alt=alt, width="100%", height="11rem", object_fit="cover",
                     border_radius="0.9rem"),
            rx.hstack(
                rx.icon(icone, size=18, color=rx.color("teal", 10)),
                rx.heading(titulo, size="4", weight="bold"),
                spacing="2",
                align="center",
            ),
            rx.text(texto, size="2", color=rx.color("gray", 11)),
            spacing="2",
            align_items="start",
        ),
        width="100%",
    )


def boas_vindas_page() -> rx.Component:
    """Página inicial pública (changes `porta-de-entrada` e `boas-vindas-com-fotos`).

    Sem `on_load` que chame o Xano (D2): só redireciona quem já tem sessão.
    """
    return rx.center(
        rx.vstack(
            _capa(),
            rx.vstack(
                rx.heading("O que você encontra", size="6", weight="bold"),
                rx.grid(
                    *[_servico(*s) for s in SERVICOS_DA_CLINICA],
                    columns=rx.breakpoints(initial="1", md="3"),
                    spacing="4",
                    width="100%",
                ),
                spacing="3",
                width="100%",
                align_items="start",
            ),
            # Os caminhos continuam (D4): é por eles que a equipe chega à sua entrada.
            rx.vstack(
                rx.heading("Por onde começar", size="6", weight="bold"),
                rx.grid(
                    _caminho("heart", "Sou cliente",
                             "Veja seus animais e marque atendimentos.",
                             "Entrar", "/entrar"),
                    _caminho("stethoscope", "Sou da equipe",
                             "Agenda do dia, serviços, colaboradores e clientes.",
                             "Entrada da equipe", "/entrar/equipe", "soft"),
                    _caminho("user-plus", "Primeira vez?",
                             "Crie sua conta de cliente em um minuto.",
                             "Criar conta", "/cadastro", "outline"),
                    columns=rx.breakpoints(initial="1", md="3"),
                    spacing="4",
                    width="100%",
                ),
                spacing="3",
                width="100%",
                align_items="start",
            ),
            # Horário e contato (change `horario-e-contato`).
            rx.card(
                rx.vstack(
                    rx.heading("Horário e contato", size="5", weight="bold"),
                    horario_e_contato(centralizado=True),
                    spacing="3",
                    align="center",
                    width="100%",
                    padding="0.5rem",
                ),
                width="100%",
            ),
            spacing="8",
            width="100%",
            max_width="64rem",
        ),
        min_height="100vh",
        padding=rx.breakpoints(initial="1.5rem 1rem", md="3rem 1.5rem"),
        width="100%",
    )


def _formulario_de_entrada(*, titulo: str, subtitulo: str,
                           rodape: rx.Component) -> rx.Component:
    """O MESMO formulário e o MESMO manipulador nas duas entradas (D1).

    Isso não é economia de código: é o que faz a verificação, o número de
    requisições e o tempo de resposta serem iguais nas duas **por
    construção**. Nada sobre a página é enviado ao servidor, e o destino vem
    só do papel da conta (change `porta-de-entrada`, D1). Se as duas
    verificassem de jeitos diferentes, descobrir quem é da equipe seria tentar
    o mesmo e-mail nas duas e ver em qual passa.
    """
    return _casca(
        campo(
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
        _campo_senha(
            "Senha",
            "Sua senha",
            AuthState.login_senha,
            AuthState.set_login_senha,
            AuthState.tipo_senha,
            AuthState.icone_senha,
            AuthState.alternar_senha,
        ),
        titulo=titulo,
        subtitulo=subtitulo,
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
        rodape=rx.vstack(
            rodape,
            rx.link("← Voltar ao início", href="/boas-vindas", size="1",
                    color=rx.color("gray", 11)),
            spacing="3",
            align_items="start",
        ),
    )


def cadastro_page() -> rx.Component:
    return _casca(
        campo(
            "Nome completo",
            rx.input(
                placeholder="Como podemos te chamar",
                value=AuthState.cad_nome,
                on_change=AuthState.set_cad_nome,
                size="3",
                width="100%",
            ),
        ),
        campo(
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
        campo(
            "Documento (CPF)",
            rx.input(
                placeholder="000.000.000-00",
                value=AuthState.cad_documento,
                on_change=AuthState.set_cad_documento,
                size="3",
                width="100%",
            ),
        ),
        campo(
            "Telefone",
            rx.input(
                placeholder="(00) 00000-0000 (opcional)",
                value=AuthState.cad_telefone,
                on_change=AuthState.set_cad_telefone,
                size="3",
                width="100%",
            ),
        ),
        campo(
            "Endereço",
            rx.input(
                placeholder="Rua, número, bairro (opcional)",
                value=AuthState.cad_endereco,
                on_change=AuthState.set_cad_endereco,
                size="3",
                width="100%",
            ),
        ),
        _campo_senha(
            "Senha",
            "Mínimo 8 caracteres",
            AuthState.cad_senha,
            AuthState.set_cad_senha,
            AuthState.tipo_cad_senha,
            AuthState.icone_cad_senha,
            AuthState.alternar_cad_senha,
        ),
        _campo_senha(
            "Confirmar senha",
            "Repita a senha",
            AuthState.cad_confirmar,
            AuthState.set_cad_confirmar,
            AuthState.tipo_cad_senha,
            AuthState.icone_cad_senha,
            AuthState.alternar_cad_senha,
        ),
        # A regra aparece antes de o erro acontecer: descobri-la por tentativa
        # e erro é o que faz gente desistir do cadastro.
        rx.text(
            "A senha precisa de pelo menos 8 caracteres, com uma letra e um número.",
            size="1",
            color=rx.color("gray", 11),
        ),
        titulo="Criar conta",
        subtitulo="Cadastre-se para acompanhar os seus pets.",
        rotulo_envio="Criar conta",
        on_submit=AuthState.cadastrar,
        rodape=rx.hstack(
            rx.text("Já tem conta?", size="2", color=rx.color("gray", 11)),
            rx.link("Entrar", href="/entrar", size="2", weight="medium"),
            spacing="2",
        ),
    )
