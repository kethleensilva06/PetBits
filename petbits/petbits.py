"""PetBits — sistema de gestão para clínica veterinária e petshop."""

import reflex as rx

from petbits.pages.agendamentos import agendamentos_page
from petbits.pages.cadastro import cadastro_page
from petbits.pages.clientes import clientes_page
from petbits.pages.erros import nao_encontrada_page, sem_permissao_page
from petbits.pages.funcionarios import funcionarios_page
from petbits.pages.index import index
from petbits.pages.login import login_page
from petbits.pages.pedidos import pedidos_page
from petbits.pages.portal import (
    portal_agendar_page,
    portal_consultas_page,
    portal_historico_page,
    portal_page,
    portal_pedidos_page,
    portal_pets_page,
)
from petbits.pages.pets import pets_page
from petbits.pages.produtos import produtos_page
from petbits.pages.prontuarios import prontuarios_page
from petbits.pages.servicos import servicos_page
from petbits.states.agendamento_state import AgendamentoState
from petbits.states.auth_state import AuthState
from petbits.states.cliente_state import ClienteState
from petbits.states.dashboard_state import DashboardState
from petbits.states.funcionario_state import FuncionarioState
from petbits.states.pedido_state import PedidoState
from petbits.states.pet_state import PetState
from petbits.states.portal_state import PortalState
from petbits.states.produto_state import ProdutoState
from petbits.states.prontuario_state import ProntuarioState
from petbits.states.servico_state import ServicoState

# Inter para corpo e tabelas (altura de x alta, dígitos tabulares, 1/l/I
# distinguíveis — o que importa em CPF e preço); Nunito para títulos e marca,
# que é onde a leitura é lenta e cabe personalidade.
FONTES = (
    "https://fonts.googleapis.com/css2"
    "?family=Inter:wght@400;500;600"
    "&family=Nunito:wght@600;700;800"
    "&display=swap"
)

app = rx.App(
    stylesheets=["/petbits.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="anonymous",
        ),
        rx.el.link(rel="stylesheet", href=FONTES),
        # Navegadores modernos preferem o SVG; o favicon.ico fica de fallback.
        rx.el.link(rel="icon", type="image/svg+xml", href="/favicon.svg"),
    ],
    html_lang="pt-BR",
)

# As nove telas da clínica. `carregar_sessao` vem primeiro em todas: ele
# revalida o token quando o backend não lembra mais deste navegador.
#
# Ele não substitui a guarda de dentro do `load_*`: `rx.redirect` é evento de
# frontend e não cancela o que já está na fila do backend, então o `load_*`
# roda de qualquer jeito. Quem barra de fato é o `_token()` lá dentro; este
# `on_load` só evita a tela piscar antes do redirect.
PAGINAS_ADMIN = [
    ("/", index, "Painel", DashboardState.load_dashboard),
    ("/clientes", clientes_page, "Clientes", ClienteState.load_clientes),
    ("/pets", pets_page, "Pets", PetState.load_pets),
    ("/agendamentos", agendamentos_page, "Agendamentos", AgendamentoState.load_agendamentos),
    ("/prontuarios", prontuarios_page, "Prontuários", ProntuarioState.load_prontuarios),
    ("/servicos", servicos_page, "Serviços", ServicoState.load_servicos),
    ("/produtos", produtos_page, "Produtos", ProdutoState.load_produtos),
    ("/pedidos", pedidos_page, "Pedidos", PedidoState.load_pedidos),
    ("/funcionarios", funcionarios_page, "Funcionários", FuncionarioState.load_funcionarios),
]

for rota, componente, titulo, carregar in PAGINAS_ADMIN:
    app.add_page(
        componente,
        route=rota,
        title=f"PetBits | {titulo}",
        on_load=[AuthState.carregar_sessao, carregar],
    )

# Porta de entrada. `redirecionar_se_logado` evita mostrar o formulário a quem
# já entrou — voltar para o login por engano e ver campos vazios passa a
# impressão de que a sessão caiu.
app.add_page(
    login_page,
    route="/login",
    title="PetBits | Entrar",
    on_load=AuthState.redirecionar_se_logado,
)
app.add_page(
    cadastro_page,
    route="/cadastro",
    title="PetBits | Criar conta",
    on_load=AuthState.redirecionar_se_logado,
)

app.add_page(
    sem_permissao_page, route="/sem-permissao", title="PetBits | Área restrita"
)
app.add_page(
    nao_encontrada_page, route="/404", title="PetBits | Página não encontrada"
)

# O portal do tutor. Mesmo desenho do painel, com uma diferença: a guarda
# passa `admin=False`, então quem entra é qualquer pessoa logada — e o que ela
# vê é recortado pela ficha de cliente dela, no servidor.
PAGINAS_PORTAL = [
    ("/portal", portal_page, "Portal", PortalState.load_inicio),
    ("/portal/pets", portal_pets_page, "Meus pets", PortalState.load_pets),
    ("/portal/agendar", portal_agendar_page, "Marcar consulta", PortalState.load_agendar),
    ("/portal/consultas", portal_consultas_page, "Minhas consultas", PortalState.load_consultas),
    ("/portal/historico", portal_historico_page, "Histórico", PortalState.load_historico),
    ("/portal/pedidos", portal_pedidos_page, "Minhas compras", PortalState.load_compras),
]

for rota, componente, titulo, carregar in PAGINAS_PORTAL:
    app.add_page(
        componente,
        route=rota,
        title=f"PetBits | {titulo}",
        on_load=[AuthState.carregar_sessao, carregar],
    )
