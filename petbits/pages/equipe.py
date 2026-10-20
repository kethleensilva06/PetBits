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

from petbits import esqueletos
from petbits.states.auth_state import AuthState
from petbits.painel import ESTOQUE_BAIXO, PEDIDOS_ESPERANDO
from petbits.pages.historico import dialogo_form_atendimento, dialogo_historico_equipe
from petbits.states.historico_state import HistoricoEquipeState
from petbits.states.equipe_state import (FUNCAO_LEGIVEL, FUNCOES, ID_UPLOAD_PRODUTO,
                                         EquipeState)
from petbits.states.loja_state import CATEGORIAS as CATEGORIAS_PRODUTO
from petbits.visual import barra, campo, marca, pilula, sair, titulo_de_pagina

AREAS = [
    ("/equipe", "Painel", "layout-dashboard"),
    ("/equipe/agenda", "Agenda", "calendar-days"),
    ("/equipe/colaboradores", "Colaboradores", "users"),
    ("/equipe/servicos", "Serviços", "scissors"),
    ("/equipe/produtos", "Produtos", "package"),
    ("/equipe/pedidos", "Pedidos", "receipt"),
    ("/equipe/balcao", "Balcão", "store"),
    ("/equipe/tutores", "Tutores", "contact"),
    ("/equipe/animais", "Animais", "paw-print"),
]




def _navegacao(atual: str) -> rx.Component:
    """Abas na tela larga; no celular, um botão que abre a lista (change
    `acabamentos-de-tela`, D3). As 9 abas quebravam em 3 linhas no celular."""
    rotulo_atual, icone_atual = next(
        ((rotulo, icone) for rota, rotulo, icone in AREAS if rota == atual),
        ("Menu", "menu"),
    )
    abas = rx.hstack(
        *[pilula(rotulo, icone, rota, rota == atual) for rota, rotulo, icone in AREAS],
        spacing="1",
        wrap="wrap",
        width="100%",
        display=rx.breakpoints(initial="none", md="flex"),
    )
    menu = rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon("menu", size=16),
                rx.icon(icone_atual, size=15),
                rotulo_atual,
                rx.icon("chevron-down", size=14),
                variant="soft",
                size="3",
                width="100%",
                justify="start",
            ),
        ),
        rx.menu.content(
            *[
                rx.menu.item(
                    rx.link(
                        rx.hstack(rx.icon(icone, size=15), rx.text(rotulo), spacing="2",
                                  align="center"),
                        href=rota,
                        underline="none",
                        color="inherit",
                        width="100%",
                    ),
                    color=rx.color("teal", 11) if rota == atual else None,
                )
                for rota, rotulo, icone in AREAS
            ],
            min_width="14rem",
        ),
    )
    return rx.box(
        abas,
        rx.box(menu, display=rx.breakpoints(initial="block", md="none"), width="100%"),
        width="100%",
        padding_bottom="0.75rem",
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
            barra(
                marca("/equipe"),
                # No celular o topo tem de caber numa linha: os selos e o nome somem
                # abaixo de `sm`, e ficam a marca, o avatar e o sair.
                rx.badge("Clínica", variant="soft", color_scheme="orange", radius="full",
                         display=rx.breakpoints(initial="none", sm="inline-flex")),
                rx.spacer(),
                rx.badge(AuthState.papel_exibido, variant="soft", radius="full",
                         display=rx.breakpoints(initial="none", sm="inline-flex")),
                # Tocar no próprio avatar abre o perfil (change `perfil-do-colaborador`).
                rx.link(
                    rx.hstack(
                        rx.avatar(src=AuthState.usuario_foto, fallback=AuthState.iniciais,
                                  radius="full", size="3", color_scheme="teal",
                                  variant="solid", custom_attrs={"alt": "Sua foto de perfil"}),
                        rx.text(AuthState.primeiro_nome, size="2",
                                color=rx.color("gray", 11),
                                display=rx.breakpoints(initial="none", sm="block")),
                        spacing="2",
                        align="center",
                    ),
                    href="/equipe/perfil",
                    aria_label="Meu perfil",
                    title="Meu perfil",
                    underline="none",
                ),
                sair(),
            ),
            _navegacao(rota),
            rx.hstack(
                titulo_de_pagina(titulo, subtitulo),
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
            padding_y="2rem",
            width="100%",
        ),
        size="4",
    )


def _carregando(oque: str) -> rx.Component:
    """Enquanto a lista não chegou, não dizer que ela está vazia."""
    return esqueletos.linhas(f"Carregando {oque}...")


def _vazio(titulo: str, recado: str, acao: rx.Component | None = None) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(titulo, size="4"),
            rx.text(recado, size="2", color=rx.color("gray", 11)),
            acao if acao is not None else rx.fragment(),
            spacing="3",
            align="center",
            width="100%",
            padding="2.5rem",
        ),
        width="100%",
    )


def _busca(placeholder: str) -> rx.Component:
    """O campo de busca das listas (change `busca-na-clinica`): filtra o que já
    está na tela, sem requisição."""
    return rx.input(
        rx.input.slot(rx.icon("search", size=16)),
        placeholder=placeholder,
        custom_attrs={"aria-label": placeholder},
        value=EquipeState.busca,
        on_change=EquipeState.set_busca,
        size="3",
        width="100%",
    )


def _lista_com_busca(tem, visiveis, cartao, vazio, oque: str, placeholder: str) -> rx.Component:
    """A lista com busca. "Nada encontrado" é diferente de "lista vazia": a
    clínica tem registros, a busca é que não achou."""
    return rx.vstack(
        rx.cond(tem, _busca(placeholder)),
        _lista(tem, visiveis, cartao, vazio, oque),
        rx.cond(
            tem & (visiveis.length() == 0),
            rx.text("Nada encontrado para “", EquipeState.busca, "”.", size="2",
                    color=rx.color("gray", 11)),
        ),
        spacing="3",
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


def _linha_de_hoje(a: dict) -> rx.Component:
    """Um agendamento de hoje no painel (change `painel-do-dia`): sem o
    telefone do tutor, que fica na Agenda (D3)."""
    return rx.hstack(
        rx.text(a["horario"], weight="bold", min_width="3.5rem"),
        rx.vstack(
            rx.text(a["animal"], " — ", a["servico"], weight="medium", size="2"),
            rx.text(a["tutor"], " · com ", a["profissional"], size="1",
                    color=rx.color("gray", 11)),
            spacing="0",
            align_items="start",
        ),
        rx.spacer(),
        rx.badge(a["situacao"], radius="full",
                 color_scheme=rx.cond(a["concluido"], "gray", "teal")),
        width="100%",
        align="center",
        padding_y="0.55rem",
        border_bottom=f"1px solid {rx.color('gray', 4)}",
        opacity=rx.cond(a["concluido"], "0.6", "1"),
    )


def _hoje() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("calendar-check", size=18, color=rx.color("accent", 10)),
                rx.heading("Hoje", size="4"),
                rx.spacer(),
                rx.link(rx.button("Abrir a agenda", variant="soft", size="1"),
                        href="/equipe/agenda"),
                width="100%",
                align="center",
            ),
            rx.cond(
                EquipeState.tem_painel_agenda,
                rx.vstack(rx.foreach(EquipeState.painel_agenda, _linha_de_hoje),
                          spacing="0", width="100%"),
                rx.text("Ninguém marcado para hoje.", size="2",
                        color=rx.color("gray", 11), padding_y="0.5rem"),
            ),
            spacing="2",
            width="100%",
        ),
        width="100%",
    )


def _pedido_esperando(situacao: str, rotulo: str, icone: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.icon(icone, size=20, color=rx.color("orange", 10)),
            rx.vstack(
                rx.heading(EquipeState.painel_pedidos[situacao], size="6"),
                rx.text(rotulo, size="2", color=rx.color("gray", 11)),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            align="center",
        ),
        on_click=EquipeState.abrir_pedidos(situacao),
        cursor="pointer",
        width="100%",
        _hover={"background": rx.color("gray", 2)},
    )


def _estoque_do_painel(chave: str, rotulo: str, icone: str, cor: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.icon(icone, size=20, color=rx.color(cor, 10)),
            rx.vstack(
                rx.heading(EquipeState.painel_estoque[chave], size="6"),
                rx.text(rotulo, size="2", color=rx.color("gray", 11)),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            align="center",
        ),
        on_click=EquipeState.abrir_estoque_baixo,
        cursor="pointer",
        width="100%",
        _hover={"background": rx.color("gray", 2)},
    )


def _pedidos_esperando() -> rx.Component:
    return rx.vstack(
        rx.heading("Pedidos esperando a equipe", size="4"),
        *[_pedido_esperando(situacao, rotulo, icone)
          for _chave, situacao, rotulo, icone in PEDIDOS_ESPERANDO],
        # Estoque (change `estoque-baixo`): os dois abrem Produtos filtrado.
        rx.heading("Estoque", size="4", padding_top="0.5rem"),
        rx.grid(
            _estoque_do_painel("esgotados", "Esgotados", "package-x", "red"),
            _estoque_do_painel("acabando", f"Com {ESTOQUE_BAIXO} ou menos", "package-minus",
                               "amber"),
            columns="2",
            spacing="2",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )


def painel_page() -> rx.Component:
    return _casca(
        rx.cond(
            EquipeState.painel_carregado,
            rx.vstack(
                rx.grid(
                    _hoje(),
                    _pedidos_esperando(),
                    columns=rx.breakpoints(initial="1", md="2fr 1fr"),
                    spacing="4",
                    width="100%",
                    align_items="start",
                ),
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
                rx.button(rx.icon("refresh-cw", size=14), "Atualizar", variant="ghost",
                          size="1", on_click=EquipeState.carregar_painel,
                          disabled=EquipeState.carregando),
                spacing="4",
                width="100%",
            ),
            rx.cond(EquipeState.carregando, _carregando("o painel")),
        ),
        # Tudo numa requisição só (change `painel-do-dia`, D1): o painel é a
        # tela inicial da equipe, e cada chamada a mais sairia de toda abertura.
        rota="/equipe",
        titulo="Painel da clínica",
        subtitulo="Quem vem hoje e o que espera a equipe.",
    )


# --- colaboradores ------------------------------------------------------------


def _cartao_colaborador(c: dict) -> rx.Component:
    # Quem foi desligado CONTINUA na lista, e isso é requisito, não descuido:
    # esconder quem saiu esconderia o único caminho de religar, e apagaria a
    # informação de que aquela pessoa trabalhou aqui — que é o motivo de
    # desligar existir em vez de excluir.
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
                    rx.text(c["telefone"], size="1", color=rx.color("gray", 11)),
                    rx.text(c["email"], size="1", color=rx.color("gray", 11)),
                    rx.text("Entrada: ", c["entrada"], size="1",
                            color=rx.color("gray", 11)),
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
                rx.hstack(
                    # Mesma linguagem visual dos produtos inativos, na change
                    # `loja`: quem aprende uma tela entende a outra.
                    rx.button(
                        rx.cond(c["ativo"], "Desligar", "Religar"),
                        on_click=lambda: EquipeState.alternar_ativo_colaborador(c),
                        variant="soft",
                        color_scheme=rx.cond(c["ativo"], "amber", "teal"),
                        size="1",
                    ),
                    rx.button(
                        "Editar",
                        on_click=lambda: EquipeState.editar_colaborador(c),
                        variant="soft",
                        size="1",
                    ),
                    spacing="2",
                ),
                rx.fragment(),
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        width="100%",
        opacity=rx.cond(c["ativo"], "1", "0.6"),
    )


def _dialogo_colaborador() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(EquipeState.titulo_col),
            rx.vstack(
                campo("Nome", rx.input(placeholder="Nome completo",
                                        value=EquipeState.col_nome,
                                        on_change=EquipeState.set_col_nome,
                                        width="100%")),
                # `rx.select` com lista de strings renderiza a string crua, e
                # o cartao ao lado ja mostra o rotulo traduzido -- "Clinico
                # geral" na lista e `clinico_geral` no seletor, no mesmo
                # clique. O mapa de rotulos ja existia duas linhas abaixo da
                # lista; faltava aplica-lo aqui.
                campo("Função", rx.select.root(
                    rx.select.trigger(width="100%"),
                    rx.select.content(
                        *[rx.select.item(FUNCAO_LEGIVEL[v], value=v) for v in FUNCOES]
                    ),
                    value=EquipeState.col_funcao,
                    on_change=EquipeState.set_col_funcao,
                    width="100%",
                )),
                rx.hstack(
                    campo("Telefone", rx.input(placeholder="Opcional",
                                                value=EquipeState.col_telefone,
                                                on_change=EquipeState.set_col_telefone,
                                                width="100%")),
                    campo("E-mail", rx.input(placeholder="Opcional", type="email",
                                              value=EquipeState.col_email,
                                              on_change=EquipeState.set_col_email,
                                              width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                campo("Entrada na clínica", rx.input(
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
        _lista_com_busca(
            EquipeState.tem_colaboradores,
            EquipeState.colaboradores_visiveis,
            _cartao_colaborador,
            _vazio(
                "Nenhum colaborador cadastrado",
                "Cadastre quem trabalha na clínica para poder montar a agenda depois.",
                rx.cond(
                    AuthState.eh_gerencia,
                    rx.button("Cadastrar colaborador",
                              on_click=EquipeState.novo_colaborador, size="3"),
                    rx.text("Peça à gerência para cadastrar.", size="2",
                            color=rx.color("gray", 11)),
                ),
            ),
            "os colaboradores",
            "Buscar por nome, função, e-mail ou telefone",
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
                    rx.badge(s["categoria"], radius="full",
                             color_scheme=rx.cond(s["_categoria"] == "", "amber", "teal")),
                    rx.cond(~s["ativo"].to(bool),
                            rx.badge("Inativo", color_scheme="gray", variant="surface",
                                     radius="full")),
                    spacing="2", align="center", wrap="wrap",
                ),
                rx.cond(
                    s["descricao"],
                    rx.text(s["descricao"], size="1", color=rx.color("gray", 11)),
                ),
                spacing="1", align_items="start",
            ),
            rx.spacer(),
            # Desligar e religar (change `desligar-servico`, D3), como em produtos.
            rx.button(rx.cond(s["ativo"], "Desativar", "Ativar"),
                      on_click=lambda: EquipeState.alternar_ativo_servico(s),
                      variant="soft", color_scheme=rx.cond(s["ativo"], "amber", "teal"),
                      size="1"),
            rx.button("Editar", on_click=lambda: EquipeState.editar_servico(s),
                      variant="soft", size="1"),
            width="100%", align="start", spacing="2",
        ),
        width="100%",
    )


def _dialogo_servico() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(EquipeState.titulo_srv),
            rx.vstack(
                campo("Nome", rx.input(placeholder="Banho e tosa, consulta...",
                                        value=EquipeState.srv_nome,
                                        on_change=EquipeState.set_srv_nome,
                                        width="100%")),
                campo("Descrição", rx.text_area(
                    placeholder="Opcional",
                    value=EquipeState.srv_descricao,
                    on_change=EquipeState.set_srv_descricao,
                    width="100%")),
                rx.hstack(
                    campo("Preço (R$)", rx.input(placeholder="0,00",
                                                  value=EquipeState.srv_preco,
                                                  on_change=EquipeState.set_srv_preco,
                                                  width="100%")),
                    campo("Duração (min)", rx.input(placeholder="30",
                                                     value=EquipeState.srv_duracao,
                                                     on_change=EquipeState.set_srv_duracao,
                                                     width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                # Change `agendamento`, D5: sem categoria, o serviço não é
                # oferecido ao tutor.
                campo("Categoria", rx.select.root(
                    rx.select.trigger(placeholder="Escolha: Clínica ou Banho e tosa",
                                      width="100%"),
                    rx.select.content(
                        rx.select.item("Clínica", value="clinica"),
                        rx.select.item("Banho e tosa", value="banho_tosa"),
                    ),
                    value=EquipeState.srv_categoria,
                    on_change=EquipeState.set_srv_categoria,
                    width="100%",
                )),
                # A duração é o que torna a agenda calculável: sem ela não há
                # como saber se dois atendimentos se sobrepõem.
                rx.text(
                    "A duração é obrigatória e maior que zero — é ela que permite "
                    "calcular a agenda. Preço zero é válido (serviço gratuito).",
                    size="1", color=rx.color("gray", 11),
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


# --- produtos da loja (change `loja`) ---------------------------------------------


def _cartao_produto(p: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            # A mesma imagem que o cliente vê na loja (change `foto-do-produto`, D4).
            rx.image(src=p["imagem"], alt=p["nome"], width="3.5rem", height="3.5rem",
                     object_fit="cover", border_radius="0.75rem", flex_shrink="0"),
            rx.vstack(
                rx.hstack(
                    rx.heading(p["nome"], size="4"),
                    rx.badge(p["categoria"], variant="soft", radius="full"),
                    rx.badge(p["preco"], color_scheme="gray", variant="soft", radius="full"),
                    # Vermelho esgotado, âmbar até 5 (change `estoque-baixo`).
                    rx.badge(p["estoque"], variant="soft", radius="full",
                             color_scheme=rx.match(p["nivel"], ("esgotado", "red"),
                                                   ("baixo", "amber"), "gray")),
                    rx.cond(p["ativo"], rx.fragment(),
                            rx.badge("Inativo", color_scheme="amber", radius="full")),
                    spacing="2", align="center", wrap="wrap",
                ),
                rx.text(p["marca"], " ", p["unidade"], size="1", color=rx.color("gray", 11)),
                rx.cond(p["descricao"],
                        rx.text(p["descricao"], size="1", color=rx.color("gray", 11))),
                spacing="1", align_items="start",
            ),
            rx.spacer(),
            rx.button(rx.cond(p["ativo"], "Desativar", "Ativar"),
                      on_click=lambda: EquipeState.alternar_ativo(p),
                      variant="soft", color_scheme=rx.cond(p["ativo"], "amber", "teal"),
                      size="1"),
            rx.button("Editar", on_click=lambda: EquipeState.editar_produto(p),
                      variant="soft", size="1"),
            width="100%", align="start", spacing="2",
        ),
        width="100%",
        opacity=rx.cond(p["ativo"], "1", "0.6"),
    )


def _foto_do_produto() -> rx.Component:
    """Foto do produto (change `foto-do-produto`, D5). Só na edição, porque a
    foto é gravada pelo id. O seletor não filtra por tipo: com `accept` e
    `max_size`, o arquivo recusado sumia sem aviso (change `perfil-e-fotos`)."""
    return rx.cond(
        EquipeState.prd_editando,
        rx.hstack(
            rx.image(src=EquipeState.prd_imagem, alt="Foto do produto",
                     width="5.5rem", height="5.5rem", object_fit="cover",
                     border_radius="1rem", flex_shrink="0"),
            rx.vstack(
                rx.upload.root(
                    rx.button(
                        rx.cond(EquipeState.prd_enviando_foto, rx.spinner(size="2"),
                                rx.icon("camera", size=16)),
                        rx.cond(EquipeState.prd_tem_foto, "Trocar foto", "Escolher foto"),
                        variant="soft",
                        disabled=EquipeState.prd_enviando_foto,
                    ),
                    id=ID_UPLOAD_PRODUTO,
                    max_files=1,
                    multiple=False,
                    no_drag=True,
                    on_drop=EquipeState.enviar_foto_produto(
                        rx.upload_files(upload_id=ID_UPLOAD_PRODUTO)),
                ),
                rx.text(rx.cond(EquipeState.prd_tem_foto,
                                "Foto enviada pela equipe. JPG, PNG ou WebP, até 5 MB.",
                                "Foto automática. JPG, PNG ou WebP, até 5 MB."),
                        size="1", color=rx.color("gray", 11)),
                rx.cond(EquipeState.prd_erro_foto,
                        rx.text(EquipeState.prd_erro_foto, size="1",
                                color=rx.color("red", 11))),
                spacing="1",
                align_items="start",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        rx.text("Depois de cadastrar, edite o produto para pôr a foto dele.",
                size="1", color=rx.color("gray", 11)),
    )


def _dialogo_produto() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(EquipeState.titulo_prd),
            rx.vstack(
                _foto_do_produto(),
                campo("Nome", rx.input(placeholder="Ração adulto 1 kg",
                                        value=EquipeState.prd_nome,
                                        on_change=EquipeState.set_prd_nome, width="100%")),
                rx.hstack(
                    campo("Categoria", rx.select.root(
                        rx.select.trigger(width="100%"),
                        rx.select.content(*[rx.select.item(rotulo, value=valor)
                                            for valor, rotulo in CATEGORIAS_PRODUTO.items()]),
                        value=EquipeState.prd_categoria,
                        on_change=EquipeState.set_prd_categoria,
                    )),
                    campo("Marca", rx.input(placeholder="Opcional",
                                             value=EquipeState.prd_marca,
                                             on_change=EquipeState.set_prd_marca,
                                             width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                rx.hstack(
                    campo("Unidade", rx.input(placeholder="un, pacote 1 kg...",
                                               value=EquipeState.prd_unidade,
                                               on_change=EquipeState.set_prd_unidade,
                                               width="100%")),
                    campo("Preço (R$)", rx.input(placeholder="49,90",
                                                  value=EquipeState.prd_preco,
                                                  on_change=EquipeState.set_prd_preco,
                                                  width="100%")),
                    campo("Estoque", rx.input(placeholder="20",
                                               value=EquipeState.prd_estoque,
                                               on_change=EquipeState.set_prd_estoque,
                                               width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                campo("Descrição", rx.text_area(placeholder="Opcional",
                                                 value=EquipeState.prd_descricao,
                                                 on_change=EquipeState.set_prd_descricao,
                                                 width="100%")),
                rx.cond(EquipeState.prd_erro,
                        rx.callout(EquipeState.prd_erro, icon="triangle_alert",
                                   color_scheme="red", size="1", width="100%")),
                rx.hstack(
                    rx.button("Cancelar", on_click=EquipeState.set_prd_dialogo(False),
                              variant="soft", color_scheme="gray"),
                    rx.button("Salvar", on_click=EquipeState.salvar_produto,
                              disabled=EquipeState.salvando),
                    justify="end", spacing="3", width="100%", padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="36rem",
        ),
        open=EquipeState.prd_dialogo,
        on_open_change=EquipeState.set_prd_dialogo,
    )


def produtos_page() -> rx.Component:
    return _casca(
        # Todos ou só o estoque baixo (change `estoque-baixo`).
        rx.cond(
            EquipeState.tem_produtos,
            rx.segmented_control.root(
                rx.segmented_control.item("Todos", value="todos"),
                rx.segmented_control.item(f"Estoque baixo (até {ESTOQUE_BAIXO})",
                                          value="baixo"),
                value=EquipeState.filtro_estoque,
                on_change=EquipeState.set_filtro_estoque,
            ),
        ),
        rx.cond(
            EquipeState.tem_produtos & (EquipeState.produtos_visiveis.length() == 0),
            rx.text("Nenhum produto ativo com estoque baixo.", size="2",
                    color=rx.color("gray", 11)),
        ),
        _lista(
            EquipeState.tem_produtos,
            EquipeState.produtos_visiveis,
            _cartao_produto,
            _vazio("Nenhum produto na loja",
                   "Cadastre o que a loja vende, com preço e estoque.",
                   rx.button("Cadastrar produto", on_click=EquipeState.novo_produto,
                             size="3")),
            "os produtos",
        ),
        _dialogo_produto(),
        rota="/equipe/produtos",
        titulo="Produtos",
        subtitulo="O catálogo da loja. Produto inativo ou sem estoque não aparece para o cliente.",
        acao=rx.cond(EquipeState.tem_produtos,
                     rx.button(rx.icon("plus", size=16), "Novo produto",
                               on_click=EquipeState.novo_produto),
                     rx.fragment()),
    )


# --- pedidos da loja (change `pedidos-da-equipe`) ---------------------------------


def _acao_pedido(pedido_id, a: dict) -> rx.Component:
    return rx.button(
        a["rotulo"],
        on_click=EquipeState.avancar_pedido(pedido_id, a["situacao"]),
        size="1",
        variant=rx.cond(a["situacao"] == "cancelado", "soft", "solid"),
        color_scheme=rx.cond(a["situacao"] == "cancelado", "red", "teal"),
    )


def _cartao_pedido(p: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text("Pedido nº ", p["id"], weight="bold"),
                rx.badge(p["situacao"], radius="full"),
                rx.cond(p["pago"], rx.badge("Pagamento registrado", color_scheme="green",
                                            variant="soft", radius="full")),
                rx.spacer(),
                rx.text(p["total"], weight="bold"),
                width="100%", align="center", wrap="wrap",
            ),
            rx.text(p["cliente"], size="2"),
            rx.text(p["quando"], " · ", p["origem"], " · ", p["entrega"], " · ",
                    p["pagamento"], size="1", color=rx.color("gray", 11)),
            rx.cond(p["endereco"], rx.text("Entregar em: ", p["endereco"], size="1",
                                           color=rx.color("gray", 11))),
            rx.foreach(p["itens"].to(list[dict]), lambda i: rx.hstack(
                rx.text(i["texto"], size="2"), rx.spacer(), rx.text(i["linha"], size="2"),
                width="100%")),
            rx.hstack(
                rx.foreach(p["acoes"].to(list[dict]), lambda a: _acao_pedido(p["id"], a)),
                spacing="2", wrap="wrap", padding_top="0.25rem",
            ),
            spacing="1", width="100%", align_items="start",
        ),
        width="100%",
    )


def pedidos_equipe_page() -> rx.Component:
    return _casca(
        rx.select.root(
            rx.select.trigger(),
            rx.select.content(
                rx.select.item("Todos", value="todos"),
                rx.select.item("Aguardando pagamento", value="pendente"),
                rx.select.item("Pagos", value="pago"),
                rx.select.item("Prontos para retirada", value="pronto_retirada"),
                rx.select.item("Enviados", value="enviado"),
                rx.select.item("Entregues", value="entregue"),
                rx.select.item("Cancelados", value="cancelado"),
            ),
            value=EquipeState.filtro_pedidos,
            on_change=EquipeState.set_filtro_pedidos,
        ),
        _lista_com_busca(
            EquipeState.tem_pedidos_clinica,
            EquipeState.pedidos_visiveis,
            _cartao_pedido,
            _vazio("Nenhum pedido", "Os pedidos feitos na loja aparecem aqui."),
            "os pedidos",
            "Buscar por número, cliente, telefone ou produto",
        ),
        rota="/equipe/pedidos",
        titulo="Pedidos",
        subtitulo="Os pedidos da loja. Cancelar devolve os itens ao estoque.",
    )


# --- venda no balcão (change `venda-no-balcao`) -----------------------------------


def _produto_balcao(p: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(p["nome"], weight="medium", size="2"),
                rx.text(p["preco"], " · ", p["estoque"], size="1", color=rx.color("gray", 11)),
                spacing="0", align_items="start",
            ),
            rx.spacer(),
            rx.icon_button(rx.icon("plus", size=14), size="1",
                           on_click=EquipeState.balcao_adicionar(p["id"]),
                           aria_label="Adicionar à venda"),
            width="100%", align="center",
        ),
        width="100%",
    )


def _item_balcao(i: dict) -> rx.Component:
    return rx.hstack(
        rx.text(i["nome"], size="2", flex="1"),
        rx.icon_button(rx.icon("minus", size=14), size="1", variant="soft",
                       on_click=EquipeState.balcao_tirar(i["id"]), aria_label="Tirar um"),
        rx.text(i["quantidade"], size="2", min_width="1.5rem", text_align="center"),
        rx.icon_button(rx.icon("plus", size=14), size="1", variant="soft",
                       on_click=EquipeState.balcao_adicionar(i["id"].to(int)),
                       disabled=~i["pode_mais"].to(bool), aria_label="Mais um"),
        rx.text(i["linha"], size="2", min_width="6rem", text_align="right"),
        width="100%", align="center", spacing="2",
    )


def balcao_page() -> rx.Component:
    return _casca(
        rx.cond(EquipeState.balcao_aviso,
                rx.callout(EquipeState.balcao_aviso, icon="circle_check",
                           color_scheme="green", size="1", width="100%")),
        rx.grid(
            rx.vstack(
                rx.text("Produtos à venda", weight="bold"),
                rx.cond(
                    EquipeState.produtos_a_venda.length() > 0,
                    rx.grid(rx.foreach(EquipeState.produtos_a_venda, _produto_balcao),
                            columns=rx.breakpoints(initial="1", sm="2"), spacing="2",
                            width="100%"),
                    rx.text("Nenhum produto ativo com estoque.", size="2",
                            color=rx.color("gray", 11)),
                ),
                spacing="2", width="100%", align_items="start",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Venda", weight="bold"),
                    rx.select.root(
                        rx.select.trigger(placeholder="Escolha o cliente", width="100%"),
                        rx.select.content(rx.foreach(
                            EquipeState.tutores,
                            lambda t: rx.select.item(t["nome"], " · ", t["documento"],
                                                     value=t["id"].to_string()))),
                        value=EquipeState.balcao_cliente,
                        on_change=EquipeState.set_balcao_cliente,
                        width="100%",
                    ),
                    rx.foreach(EquipeState.itens_balcao, _item_balcao),
                    rx.divider(),
                    rx.hstack(rx.text("Total"), rx.spacer(),
                              rx.text(EquipeState.total_balcao, weight="bold"), width="100%"),
                    rx.text("A venda é registrada como entregue e paga na loja, na conta do "
                            "cliente.", size="1", color=rx.color("gray", 11)),
                    rx.cond(EquipeState.balcao_erro,
                            rx.callout(EquipeState.balcao_erro, icon="triangle_alert",
                                       color_scheme="red", size="1", width="100%")),
                    rx.button("Confirmar venda", on_click=EquipeState.confirmar_venda,
                              disabled=EquipeState.salvando, size="3", width="100%"),
                    spacing="2", width="100%",
                ),
                width="100%",
            ),
            columns=rx.breakpoints(initial="1", md="3fr 2fr"),
            spacing="4", width="100%", align_items="start",
        ),
        rota="/equipe/balcao",
        titulo="Venda no balcão",
        subtitulo="Venda presencial, registrada na conta do cliente.",
    )


# --- agenda do dia (change `agendamento`) -----------------------------------------


def _nao_compareceu(a: dict) -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(rx.icon("user-x", size=14), "Não compareceu", variant="soft",
                      color_scheme="gray", size="1"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Registrar falta?"),
            rx.alert_dialog.description(
                a["animal"], " · ", a["servico"], " · ", a["horario"],
                ". A falta não se desfaz por aqui.",
            ),
            rx.hstack(
                rx.alert_dialog.cancel(rx.button("Voltar", variant="soft", color_scheme="gray")),
                rx.alert_dialog.action(rx.button("Registrar falta",
                                                 on_click=EquipeState.marcar_falta(a["id"]))),
                spacing="3",
                justify="end",
                padding_top="1rem",
            ),
        ),
    )


def _item_da_agenda(a: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.text(a["horario"], weight="bold", min_width="6.5rem"),
            rx.vstack(
                rx.hstack(
                    rx.text(a["servico"], weight="medium"),
                    rx.badge(a["situacao"], radius="full",
                             color_scheme=rx.cond(a["cancelado"], "gray",
                                                  rx.cond(a["faltou"], "amber", "teal"))),
                    spacing="2", align="center", wrap="wrap",
                ),
                rx.text(a["animal"], " — ", a["tutor"], size="2",
                        color=rx.color("gray", 11)),
                rx.text("Com ", a["profissional"], size="1", color=rx.color("gray", 11)),
                rx.cond(a["observacoes"],
                        rx.text(a["observacoes"], size="1", color=rx.color("gray", 11))),
                spacing="1", align_items="start",
            ),
            rx.spacer(),
            rx.hstack(
                # Registrar daqui conclui o agendamento (change `historico-clinico`, D4).
                rx.cond(a["marcado"],
                        rx.button(rx.icon("stethoscope", size=14), "Registrar atendimento",
                                  on_click=HistoricoEquipeState.da_agenda(a), variant="soft",
                                  size="1")),
                # Só depois que o horário começou (change `nao-compareceu`).
                rx.cond(a["pode_faltar"], _nao_compareceu(a)),
                spacing="2",
                wrap="wrap",
            ),
            spacing="4", align="start", width="100%", wrap="wrap",
            opacity=rx.cond(a["cancelado"], "0.55", "1"),
        ),
        width="100%",
    )


def agenda_equipe_page() -> rx.Component:
    return _casca(
        rx.hstack(
            rx.icon_button(rx.icon("chevron_left"), variant="soft",
                           on_click=EquipeState.mudar_dia_da_agenda(-1),
                           aria_label="Dia anterior"),
            rx.text(EquipeState.agenda_titulo, weight="bold", size="4"),
            rx.icon_button(rx.icon("chevron_right"), variant="soft",
                           on_click=EquipeState.mudar_dia_da_agenda(1),
                           aria_label="Próximo dia"),
            rx.button("Hoje", variant="ghost", on_click=EquipeState.agenda_de_hoje),
            spacing="3", align="center",
        ),
        _lista(
            EquipeState.tem_agenda,
            EquipeState.agenda,
            _item_da_agenda,
            _vazio("Nenhum agendamento neste dia",
                   "Os agendamentos marcados pelos tutores aparecem aqui."),
            "a agenda",
        ),
        dialogo_form_atendimento(),
        rota="/equipe/agenda",
        titulo="Agenda",
        subtitulo="Os agendamentos do dia, de todos os profissionais. Registre o "
                  "atendimento direto do agendamento.",
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
                rx.text(t["telefone"], size="1", color=rx.color("gray", 11)),
                rx.text(t["email"], size="1", color=rx.color("gray", 11)),
                spacing="4", wrap="wrap",
            ),
            rx.text(t["endereco"], size="1", color=rx.color("gray", 11)),
            spacing="1", align_items="start", width="100%",
        ),
        width="100%",
    )


def _dialogo_tutor() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Novo tutor"),
            rx.vstack(
                campo("Nome", rx.input(placeholder="Nome completo",
                                        value=EquipeState.tut_nome,
                                        on_change=EquipeState.set_tut_nome,
                                        width="100%")),
                rx.hstack(
                    campo("Documento (CPF)", rx.input(placeholder="000.000.000-00",
                                                       value=EquipeState.tut_documento,
                                                       on_change=EquipeState.set_tut_documento,
                                                       width="100%")),
                    campo("Telefone", rx.input(placeholder="Opcional",
                                                value=EquipeState.tut_telefone,
                                                on_change=EquipeState.set_tut_telefone,
                                                width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                campo("E-mail", rx.input(placeholder="Opcional", type="email",
                                          value=EquipeState.tut_email,
                                          on_change=EquipeState.set_tut_email,
                                          width="100%")),
                campo("Endereco", rx.input(placeholder="Opcional",
                                            value=EquipeState.tut_endereco,
                                            on_change=EquipeState.set_tut_endereco,
                                            width="100%")),
                # O aviso aparece ANTES de salvar, e nao depois. Quem cadastra
                # precisa saber na hora que esta ocupando o documento daquela
                # pessoa sem lhe dar acesso -- descobrir isso depois, quando ela
                # tentar se cadastrar e for recusada sem explicacao, e o que
                # este texto existe para evitar.
                rx.callout(
                    "Este tutor nao tera acesso ao aplicativo. O documento fica "
                    "reservado para ele, entao, se a pessoa tentar se cadastrar "
                    "sozinha depois, o cadastro sera recusado ate a clinica ligar "
                    "uma conta a ficha.",
                    icon="info", size="1", width="100%",
                ),
                rx.cond(
                    EquipeState.tut_erro,
                    rx.callout(EquipeState.tut_erro, icon="triangle_alert",
                               color_scheme="red", size="1", width="100%"),
                ),
                rx.hstack(
                    rx.button("Cancelar", on_click=EquipeState.fechar_tutor,
                              variant="soft", color_scheme="gray"),
                    rx.button("Salvar", on_click=EquipeState.salvar_tutor,
                              disabled=EquipeState.salvando),
                    justify="end", spacing="3", width="100%", padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="34rem",
        ),
        open=EquipeState.tut_dialogo,
        on_open_change=EquipeState.set_tut_dialogo,
    )


def tutores_page() -> rx.Component:
    return _casca(
        _lista_com_busca(
            EquipeState.tem_tutores,
            EquipeState.tutores_visiveis,
            _cartao_tutor,
            _vazio("Nenhum tutor cadastrado",
                   "Cadastre quem chega no balcao, ou espere os tutores criarem "
                   "conta no aplicativo.",
                   rx.button("Cadastrar tutor", on_click=EquipeState.novo_tutor,
                             size="3")),
            "os tutores",
            "Buscar por nome, CPF, telefone ou e-mail",
        ),
        _dialogo_tutor(),
        rota="/equipe/tutores",
        titulo="Tutores",
        subtitulo="Todos os clientes da clínica, inclusive os que não têm conta de acesso.",
        acao=rx.cond(
            EquipeState.tem_tutores,
            rx.button(rx.icon("plus", size=16), "Novo tutor",
                      on_click=EquipeState.novo_tutor),
            rx.fragment(),
        ),
    )


def _cartao_animal(a: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(a["nome"], size="4"),
                rx.badge(a["especie"], variant="soft", radius="full", color_scheme="orange"),
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
                rx.text(a["raca"], size="1", color=rx.color("gray", 11)),
                rx.text("Nasc.: ", a["nascimento"], size="1",
                        color=rx.color("gray", 11)),
                rx.text("Peso: ", a["peso"], " kg", size="1",
                        color=rx.color("gray", 11)),
                spacing="4", wrap="wrap",
            ),
            # O histórico clínico (change `historico-clinico`, D5).
            rx.button(rx.icon("clipboard-list", size=14), "Histórico",
                      on_click=HistoricoEquipeState.abrir(a), variant="soft", size="1",
                      margin_top="0.25rem"),
            spacing="1", align_items="start", width="100%",
        ),
        width="100%",
    )


def _dialogo_animal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Novo animal"),
            rx.vstack(
                # De quem e o animal vem PRIMEIRO: e o campo que o caminho do
                # tutor nao tem, e o unico cuja ausencia cria um registro
                # invisivel para o dono.
                campo("Tutor responsavel", rx.select(
                    EquipeState.opcoes_de_tutor,
                    placeholder="Escolha o tutor",
                    value=EquipeState.ani_tutor,
                    on_change=EquipeState.set_ani_tutor,
                    width="100%",
                )),
                campo("Nome", rx.input(placeholder="Nome do animal",
                                        value=EquipeState.ani_nome,
                                        on_change=EquipeState.set_ani_nome,
                                        width="100%")),
                rx.hstack(
                    campo("Especie", rx.input(placeholder="Cao, gato...",
                                               value=EquipeState.ani_especie,
                                               on_change=EquipeState.set_ani_especie,
                                               width="100%")),
                    campo("Raca", rx.input(placeholder="Opcional",
                                            value=EquipeState.ani_raca,
                                            on_change=EquipeState.set_ani_raca,
                                            width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                rx.hstack(
                    campo("Nascimento", rx.input(type="date",
                                                  value=EquipeState.ani_nascimento,
                                                  on_change=EquipeState.set_ani_nascimento,
                                                  width="100%")),
                    campo("Peso (kg)", rx.input(placeholder="Opcional",
                                                 value=EquipeState.ani_peso,
                                                 on_change=EquipeState.set_ani_peso,
                                                 width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                campo("Observacoes", rx.text_area(
                    placeholder="Alergias, cuidados especiais...",
                    value=EquipeState.ani_observacoes,
                    on_change=EquipeState.set_ani_observacoes,
                    width="100%")),
                rx.cond(
                    EquipeState.ani_erro,
                    rx.callout(EquipeState.ani_erro, icon="triangle_alert",
                               color_scheme="red", size="1", width="100%"),
                ),
                rx.hstack(
                    rx.button("Cancelar", on_click=EquipeState.fechar_animal,
                              variant="soft", color_scheme="gray"),
                    rx.button("Salvar", on_click=EquipeState.salvar_animal,
                              disabled=EquipeState.salvando),
                    justify="end", spacing="3", width="100%", padding_top="0.5rem",
                ),
                spacing="3", width="100%",
            ),
            max_width="34rem",
        ),
        open=EquipeState.ani_dialogo,
        on_open_change=EquipeState.set_ani_dialogo,
    )


def animais_page() -> rx.Component:
    return _casca(
        _lista_com_busca(
            EquipeState.tem_animais,
            EquipeState.animais_visiveis,
            _cartao_animal,
            _vazio("Nenhum animal cadastrado",
                   "Cadastre o animal de quem chega, ou espere os tutores "
                   "cadastrarem pelo aplicativo.",
                   rx.button("Cadastrar animal", on_click=EquipeState.novo_animal,
                             size="3")),
            "os animais",
            "Buscar por nome, espécie, raça ou tutor",
        ),
        _dialogo_animal(),
        dialogo_historico_equipe(),
        dialogo_form_atendimento(),
        rota="/equipe/animais",
        titulo="Animais",
        subtitulo="Todos os animais atendidos, com o tutor responsável por cada um.",
        acao=rx.cond(
            EquipeState.tem_animais,
            rx.button(rx.icon("plus", size=16), "Novo animal",
                      on_click=EquipeState.novo_animal),
            rx.fragment(),
        ),
    )
