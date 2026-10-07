"""A área da clínica: painel, colaboradores, serviços, tutores e animais.

O menu desta área se desenha a partir do papel que já está no armazenamento
local, **sem perguntar nada ao backend**. Um endpoint do tipo
`GET /equipe/sou-equipe`, para a tela perguntar antes de montar o menu,
custaria uma requisição a mais por tela — e seria, ele próprio, um oráculo de
papel chamável com qualquer token.

As telas de tutores e de animais não têm botão de criar nem de alterar, e
essa ausência é o que comunica "só leitura": a escrita da clínica sobre
tutor e animal não foi desenhada nesta change.
"""

import reflex as rx

from petbits.states.auth_state import AuthState
from petbits.states.equipe_state import FUNCAO_LEGIVEL, FUNCOES, EquipeState

AREAS = [
    ("/equipe", "Painel", "layout-dashboard"),
    ("/equipe/colaboradores", "Colaboradores", "users"),
    ("/equipe/servicos", "Serviços", "scissors"),
    ("/equipe/tutores", "Tutores", "contact"),
    ("/equipe/animais", "Animais", "paw-print"),
]


def _campo(rotulo: str, componente: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(rotulo, size="2", weight="medium"),
        componente,
        spacing="1",
        width="100%",
        align_items="start",
    )


def _navegacao(atual: str) -> rx.Component:
    return rx.hstack(
        *[
            rx.link(
                rx.hstack(
                    rx.icon(icone, size=15),
                    rx.text(rotulo, size="2"),
                    spacing="2",
                    align="center",
                ),
                href=rota,
                weight="medium" if rota == atual else "regular",
                color=rx.color("accent", 11) if rota == atual else rx.color("gray", 11),
                text_decoration="none",
            )
            for rota, rotulo, icone in AREAS
        ],
        spacing="5",
        wrap="wrap",
        width="100%",
        padding_y="0.75rem",
        border_bottom=f"1px solid {rx.color('gray', 5)}",
        margin_bottom="1.5rem",
    )


def _casca(
    *conteudo,
    rota: str,
    titulo: str,
    subtitulo: str,
    acao: rx.Component | None = None,
) -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.heading("PetBits", size="6"),
                    rx.badge("Clínica", variant="soft", radius="full"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.text(AuthState.primeiro_nome, size="2", color=rx.color("gray", 11)),
                rx.badge(AuthState.papel_exibido, variant="soft", radius="full"),
                rx.button(
                    "Sair",
                    on_click=AuthState.sair,
                    variant="soft",
                    color_scheme="gray",
                    size="2",
                ),
                width="100%",
                align="center",
            ),
            _navegacao(rota),
            rx.hstack(
                rx.vstack(
                    rx.heading(titulo, size="7"),
                    rx.text(subtitulo, color=rx.color("gray", 11), size="2"),
                    spacing="1",
                    align_items="start",
                ),
                rx.spacer(),
                acao if acao is not None else rx.fragment(),
                width="100%",
                align="center",
                padding_bottom="0.5rem",
            ),
            # O 429 chega aqui como qualquer outro erro, mas com texto que diz
            # o que fazer: o limite é por instância e compartilhado, então ele
            # deixa de ser hipótese num dia movimentado.
            rx.cond(
                EquipeState.erro,
                rx.callout(
                    EquipeState.erro,
                    icon="triangle_alert",
                    color_scheme="red",
                    size="1",
                    width="100%",
                ),
            ),
            *conteudo,
            spacing="4",
            align_items="start",
            padding_y="2.5rem",
            width="100%",
        ),
        size="4",
    )


def _carregando(oque: str) -> rx.Component:
    """Enquanto a lista não chegou, não dizer que ela está vazia."""
    return rx.center(
        rx.hstack(
            rx.spinner(size="2"),
            rx.text(f"Carregando {oque}...", size="2", color=rx.color("gray", 10)),
            spacing="2",
            align="center",
        ),
        padding="3rem",
        width="100%",
    )


def _vazio(titulo: str, recado: str, acao: rx.Component | None = None) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(titulo, size="4"),
            rx.text(recado, size="2", color=rx.color("gray", 10)),
            acao if acao is not None else rx.fragment(),
            spacing="3",
            align="center",
            width="100%",
            padding="2.5rem",
        ),
        width="100%",
    )


def _lista(tem, itens, cartao, vazio, oque: str) -> rx.Component:
    """QUATRO estados, e eles têm de ser disjuntos: tem dado, está vindo,
    está mesmo vazio, e falhou.

    O quarto é o que se esquece. Quando "carregando" é o caso padrão de tudo
    que sobra, uma requisição recusada mostra o erro **e** o spinner, lado a
    lado, para sempre — a tela contradiz a si mesma. Aqui o erro já aparece
    no callout da casca, então o corpo não mostra nada.
    """
    return rx.cond(
        tem,
        rx.vstack(rx.foreach(itens, cartao), spacing="2", width="100%"),
        rx.cond(
            EquipeState.mostrar_carregando,
            _carregando(oque),
            rx.cond(EquipeState.mostrar_vazio, vazio, rx.fragment()),
        ),
    )


# --- painel -------------------------------------------------------------------


def _contador(rotulo: str, valor, icone: str, rota: str) -> rx.Component:
    return rx.link(
        rx.card(
            rx.hstack(
                rx.icon(icone, size=22, color=rx.color("accent", 10)),
                rx.vstack(
                    rx.heading(valor, size="7"),
                    rx.text(rotulo, size="2", color=rx.color("gray", 11)),
                    spacing="0",
                    align_items="start",
                ),
                spacing="3",
                align="center",
            ),
            width="100%",
        ),
        href=rota,
        text_decoration="none",
        width="100%",
    )


def painel_page() -> rx.Component:
    return _casca(
        rx.grid(
            _contador("Colaboradores", EquipeState.total_colaboradores, "users",
                      "/equipe/colaboradores"),
            _contador("Serviços", EquipeState.total_servicos, "scissors",
                      "/equipe/servicos"),
            _contador("Tutores", EquipeState.total_tutores, "contact",
                      "/equipe/tutores"),
            _contador("Animais", EquipeState.total_animais, "paw-print",
                      "/equipe/animais"),
            columns=rx.breakpoints(initial="1", sm="2", lg="4"),
            spacing="3",
            width="100%",
        ),
        # Por que só contadores: as quatro listas no carregamento custariam
        # metade do orçamento de requisições da instância numa abertura de
        # tela. Clicar num contador abre a lista — uma requisição, quando a
        # pessoa de fato quer aquilo.
        rx.text(
            "Clique num número para abrir a lista.",
            size="1",
            color=rx.color("gray", 10),
        ),
        rota="/equipe",
        titulo="Painel da clínica",
        subtitulo="O resumo de hoje, numa requisição só.",
    )


# --- colaboradores ------------------------------------------------------------


def _cartao_colaborador(c: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading(c["nome"], size="4"),
                    rx.badge(c["funcao"], variant="soft", radius="full"),
                    rx.cond(
                        c["ativo"],
                        rx.fragment(),
                        rx.badge("Inativo", color_scheme="gray", variant="surface",
                                 radius="full"),
                    ),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.hstack(
                    rx.text(c["telefone"], size="1", color=rx.color("gray", 10)),
                    rx.text(c["email"], size="1", color=rx.color("gray", 10)),
                    rx.text("Entrada: ", c["entrada"], size="1",
                            color=rx.color("gray", 10)),
                    spacing="4",
                    wrap="wrap",
                ),
                spacing="1",
                align_items="start",
            ),
            rx.spacer(),
            # Manter o quadro e da gerencia. Esconder e CONVENIENCIA: quem
            # forjar o papel no armazenamento local ve o botao e recebe 403
            # do `exige_gerencia` em cada tentativa.
            rx.cond(
                AuthState.eh_gerencia,
                rx.button(
                    "Editar",
                    on_click=lambda: EquipeState.editar_colaborador(c),
                    variant="soft",
                    size="1",
                ),
                rx.fragment(),
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        width="100%",
    )


def _dialogo_colaborador() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(EquipeState.titulo_col),
            rx.vstack(
                _campo("Nome", rx.input(placeholder="Nome completo",
                                        value=EquipeState.col_nome,
                                        on_change=EquipeState.set_col_nome,
                                        width="100%")),
                # `rx.select` com lista de strings renderiza a string crua, e
                # o cartao ao lado ja mostra o rotulo traduzido -- "Clinico
                # geral" na lista e `clinico_geral` no seletor, no mesmo
                # clique. O mapa de rotulos ja existia duas linhas abaixo da
                # lista; faltava aplica-lo aqui.
                _campo("Função", rx.select.root(
                    rx.select.trigger(width="100%"),
                    rx.select.content(
                        *[rx.select.item(FUNCAO_LEGIVEL[v], value=v) for v in FUNCOES]
                    ),
                    value=EquipeState.col_funcao,
                    on_change=EquipeState.set_col_funcao,
                    width="100%",
                )),
                rx.hstack(
                    _campo("Telefone", rx.input(placeholder="Opcional",
                                                value=EquipeState.col_telefone,
                                                on_change=EquipeState.set_col_telefone,
                                                width="100%")),
                    _campo("E-mail", rx.input(placeholder="Opcional", type="email",
                                              value=EquipeState.col_email,
                                              on_change=EquipeState.set_col_email,
                                              width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                _campo("Entrada na clínica", rx.input(
                    type="date",
                    value=EquipeState.col_entrada,
                    on_change=EquipeState.set_col_entrada,
                    width="100%",
                )),
                rx.cond(
                    EquipeState.col_erro,
                    rx.callout(EquipeState.col_erro, icon="triangle_alert",
                               color_scheme="red", size="1", width="100%"),
                ),
                rx.hstack(
                    rx.button("Cancelar", on_click=EquipeState.fechar_colaborador,
                              variant="soft", color_scheme="gray"),
                    rx.button("Salvar", on_click=EquipeState.salvar_colaborador,
                              disabled=EquipeState.salvando),
                    justify="end", spacing="3", width="100%", padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="32rem",
        ),
        open=EquipeState.col_dialogo,
        on_open_change=EquipeState.set_col_dialogo,
    )


def colaboradores_page() -> rx.Component:
    return _casca(
        _lista(
            EquipeState.tem_colaboradores,
            EquipeState.colaboradores,
            _cartao_colaborador,
            _vazio(
                "Nenhum colaborador cadastrado",
                "Cadastre quem trabalha na clínica para poder montar a agenda depois.",
                rx.cond(
                    AuthState.eh_gerencia,
                    rx.button("Cadastrar colaborador",
                              on_click=EquipeState.novo_colaborador, size="3"),
                    rx.text("Peça à gerência para cadastrar.", size="2",
                            color=rx.color("gray", 10)),
                ),
            ),
            "os colaboradores",
        ),
        _dialogo_colaborador(),
        rota="/equipe/colaboradores",
        titulo="Colaboradores",
        subtitulo="Quem trabalha na clínica. Cadastrar aqui não cria conta de acesso.",
        acao=rx.cond(
            AuthState.eh_gerencia & EquipeState.tem_colaboradores,
            rx.button(rx.icon("plus", size=16), "Novo colaborador",
                      on_click=EquipeState.novo_colaborador),
            rx.fragment(),
        ),
    )


# --- serviços -----------------------------------------------------------------


def _cartao_servico(s: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading(s["nome"], size="4"),
                    rx.badge(s["preco"], variant="soft", radius="full"),
                    rx.badge(s["duracao"], color_scheme="gray", variant="soft",
                             radius="full"),
                    spacing="2", align="center", wrap="wrap",
                ),
                rx.cond(
                    s["descricao"],
                    rx.text(s["descricao"], size="1", color=rx.color("gray", 11)),
                ),
                spacing="1", align_items="start",
            ),
            rx.spacer(),
            rx.button("Editar", on_click=lambda: EquipeState.editar_servico(s),
                      variant="soft", size="1"),
            width="100%", align="start", spacing="3",
        ),
        width="100%",
    )


def _dialogo_servico() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(EquipeState.titulo_srv),
            rx.vstack(
                _campo("Nome", rx.input(placeholder="Banho e tosa, consulta...",
                                        value=EquipeState.srv_nome,
                                        on_change=EquipeState.set_srv_nome,
                                        width="100%")),
                _campo("Descrição", rx.text_area(
                    placeholder="Opcional",
                    value=EquipeState.srv_descricao,
                    on_change=EquipeState.set_srv_descricao,
                    width="100%")),
                rx.hstack(
                    _campo("Preço (R$)", rx.input(placeholder="0,00",
                                                  value=EquipeState.srv_preco,
                                                  on_change=EquipeState.set_srv_preco,
                                                  width="100%")),
                    _campo("Duração (min)", rx.input(placeholder="30",
                                                     value=EquipeState.srv_duracao,
                                                     on_change=EquipeState.set_srv_duracao,
                                                     width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                # A duração é o que torna a agenda calculável: sem ela não há
                # como saber se dois atendimentos se sobrepõem.
                rx.text(
                    "A duração é obrigatória e maior que zero — é ela que permite "
                    "calcular a agenda. Preço zero é válido (serviço gratuito).",
                    size="1", color=rx.color("gray", 10),
                ),
                rx.cond(
                    EquipeState.srv_erro,
                    rx.callout(EquipeState.srv_erro, icon="triangle_alert",
                               color_scheme="red", size="1", width="100%"),
                ),
                rx.hstack(
                    rx.button("Cancelar", on_click=EquipeState.fechar_servico,
                              variant="soft", color_scheme="gray"),
                    rx.button("Salvar", on_click=EquipeState.salvar_servico,
                              disabled=EquipeState.salvando),
                    justify="end", spacing="3", width="100%", padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="32rem",
        ),
        open=EquipeState.srv_dialogo,
        on_open_change=EquipeState.set_srv_dialogo,
    )


def servicos_page() -> rx.Component:
    return _casca(
        _lista(
            EquipeState.tem_servicos,
            EquipeState.servicos,
            _cartao_servico,
            _vazio(
                "Nenhum serviço cadastrado",
                "Cadastre o que a clínica oferece, com preço e duração.",
                rx.button("Cadastrar serviço", on_click=EquipeState.novo_servico,
                          size="3"),
            ),
            "os serviços",
        ),
        _dialogo_servico(),
        rota="/equipe/servicos",
        titulo="Serviços",
        subtitulo="O catálogo da clínica: o que se oferece, por quanto e em quanto tempo.",
        acao=rx.cond(
            EquipeState.tem_servicos,
            rx.button(rx.icon("plus", size=16), "Novo serviço",
                      on_click=EquipeState.novo_servico),
            rx.fragment(),
        ),
    )


# --- a visão da clínica: só leitura -------------------------------------------


def _cartao_tutor(t: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(t["nome"], size="4"),
                rx.badge(t["documento"], color_scheme="gray", variant="soft",
                         radius="full"),
                spacing="2", align="center", wrap="wrap",
            ),
            rx.hstack(
                rx.text(t["telefone"], size="1", color=rx.color("gray", 10)),
                rx.text(t["email"], size="1", color=rx.color("gray", 10)),
                spacing="4", wrap="wrap",
            ),
            rx.text(t["endereco"], size="1", color=rx.color("gray", 10)),
            spacing="1", align_items="start", width="100%",
        ),
        width="100%",
    )


def tutores_page() -> rx.Component:
    return _casca(
        _lista(
            EquipeState.tem_tutores,
            EquipeState.tutores,
            _cartao_tutor,
            _vazio("Nenhum tutor cadastrado",
                   "Os tutores aparecem aqui assim que criarem conta no aplicativo."),
            "os tutores",
        ),
        rota="/equipe/tutores",
        titulo="Tutores",
        subtitulo="Todos os clientes da clínica, inclusive os que não têm conta de acesso.",
    )


def _cartao_animal(a: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(a["nome"], size="4"),
                rx.badge(a["especie"], variant="soft", radius="full"),
                # Animal sem tutor válido é registro quebrado: para o tutor
                # ele é invisível por construção, e escondê-lo também da
                # clínica seria esconder o problema de quem pode resolvê-lo.
                rx.cond(
                    a["sem_tutor"],
                    rx.badge("Sem tutor", color_scheme="amber", variant="surface",
                             radius="full"),
                    rx.fragment(),
                ),
                spacing="2", align="center", wrap="wrap",
            ),
            rx.hstack(
                rx.text("Tutor: ", a["tutor"], size="1", color=rx.color("gray", 11)),
                rx.text(a["raca"], size="1", color=rx.color("gray", 10)),
                rx.text("Nasc.: ", a["nascimento"], size="1",
                        color=rx.color("gray", 10)),
                rx.text("Peso: ", a["peso"], " kg", size="1",
                        color=rx.color("gray", 10)),
                spacing="4", wrap="wrap",
            ),
            spacing="1", align_items="start", width="100%",
        ),
        width="100%",
    )


def animais_page() -> rx.Component:
    return _casca(
        _lista(
            EquipeState.tem_animais,
            EquipeState.animais,
            _cartao_animal,
            _vazio("Nenhum animal cadastrado",
                   "Os animais aparecem aqui conforme os tutores os cadastram."),
            "os animais",
        ),
        rota="/equipe/animais",
        titulo="Animais",
        subtitulo="Todos os animais atendidos, com o tutor responsável por cada um.",
    )
