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
from petbits.states.equipe_state import FUNCOES, EquipeState
from petbits.states.loja_state import CATEGORIAS as CATEGORIAS_PRODUTO

AREAS = [
    ("/equipe", "Painel", "layout-dashboard"),
    ("/equipe/agenda", "Agenda", "calendar-days"),
    ("/equipe/colaboradores", "Colaboradores", "users"),
    ("/equipe/servicos", "Serviços", "scissors"),
    ("/equipe/produtos", "Produtos", "package"),
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
            rx.button(
                "Editar",
                on_click=lambda: EquipeState.editar_colaborador(c),
                variant="soft",
                size="1",
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
                _campo("Função", rx.select(
                    FUNCOES,
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
                rx.button("Cadastrar colaborador",
                          on_click=EquipeState.novo_colaborador, size="3"),
            ),
            "os colaboradores",
        ),
        _dialogo_colaborador(),
        rota="/equipe/colaboradores",
        titulo="Colaboradores",
        subtitulo="Quem trabalha na clínica. Cadastrar aqui não cria conta de acesso.",
        acao=rx.cond(
            EquipeState.tem_colaboradores,
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
                # Change `agendamento`, D5: sem categoria, o serviço não é
                # oferecido ao tutor.
                _campo("Categoria", rx.select.root(
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


# --- produtos da loja (change `loja`) ---------------------------------------------


def _cartao_produto(p: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading(p["nome"], size="4"),
                    rx.badge(p["categoria"], variant="soft", radius="full"),
                    rx.badge(p["preco"], color_scheme="gray", variant="soft", radius="full"),
                    rx.badge(p["estoque"], color_scheme="gray", variant="soft", radius="full"),
                    rx.cond(p["ativo"], rx.fragment(),
                            rx.badge("Inativo", color_scheme="amber", radius="full")),
                    spacing="2", align="center", wrap="wrap",
                ),
                rx.text(p["marca"], " ", p["unidade"], size="1", color=rx.color("gray", 10)),
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


def _dialogo_produto() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(EquipeState.titulo_prd),
            rx.vstack(
                _campo("Nome", rx.input(placeholder="Ração adulto 1 kg",
                                        value=EquipeState.prd_nome,
                                        on_change=EquipeState.set_prd_nome, width="100%")),
                rx.hstack(
                    _campo("Categoria", rx.select.root(
                        rx.select.trigger(width="100%"),
                        rx.select.content(*[rx.select.item(rotulo, value=valor)
                                            for valor, rotulo in CATEGORIAS_PRODUTO.items()]),
                        value=EquipeState.prd_categoria,
                        on_change=EquipeState.set_prd_categoria,
                    )),
                    _campo("Marca", rx.input(placeholder="Opcional",
                                             value=EquipeState.prd_marca,
                                             on_change=EquipeState.set_prd_marca,
                                             width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                rx.hstack(
                    _campo("Unidade", rx.input(placeholder="un, pacote 1 kg...",
                                               value=EquipeState.prd_unidade,
                                               on_change=EquipeState.set_prd_unidade,
                                               width="100%")),
                    _campo("Preço (R$)", rx.input(placeholder="49,90",
                                                  value=EquipeState.prd_preco,
                                                  on_change=EquipeState.set_prd_preco,
                                                  width="100%")),
                    _campo("Estoque", rx.input(placeholder="20",
                                               value=EquipeState.prd_estoque,
                                               on_change=EquipeState.set_prd_estoque,
                                               width="100%")),
                    spacing="3", width="100%", align="start",
                ),
                _campo("Descrição", rx.text_area(placeholder="Opcional",
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
        _lista(
            EquipeState.tem_produtos,
            EquipeState.produtos,
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


# --- agenda do dia (change `agendamento`) -----------------------------------------


def _item_da_agenda(a: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.text(a["horario"], weight="bold", min_width="6.5rem"),
            rx.vstack(
                rx.hstack(
                    rx.text(a["servico"], weight="medium"),
                    rx.badge(a["situacao"], radius="full",
                             color_scheme=rx.cond(a["cancelado"], "gray", "teal")),
                    spacing="2", align="center", wrap="wrap",
                ),
                rx.text(a["animal"], " — ", a["tutor"], size="2",
                        color=rx.color("gray", 11)),
                rx.text("Com ", a["profissional"], size="1", color=rx.color("gray", 10)),
                rx.cond(a["observacoes"],
                        rx.text(a["observacoes"], size="1", color=rx.color("gray", 11))),
                spacing="1", align_items="start",
            ),
            spacing="4", align="start", width="100%",
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
        rota="/equipe/agenda",
        titulo="Agenda",
        subtitulo="Os agendamentos do dia, de todos os profissionais. Só leitura.",
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
