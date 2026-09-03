"""PetBits — sistema de gestão para clínica veterinária e petshop."""

import reflex as rx

from petbits.database import create_db_and_tables
from petbits.pages.agendamentos import agendamentos_page
from petbits.pages.clientes import clientes_page
from petbits.pages.funcionarios import funcionarios_page
from petbits.pages.index import index
from petbits.pages.pedidos import pedidos_page
from petbits.pages.pets import pets_page
from petbits.pages.produtos import produtos_page
from petbits.pages.prontuarios import prontuarios_page
from petbits.pages.servicos import servicos_page
from petbits.states.agendamento_state import AgendamentoState
from petbits.states.cliente_state import ClienteState
from petbits.states.dashboard_state import DashboardState
from petbits.states.funcionario_state import FuncionarioState
from petbits.states.pedido_state import PedidoState
from petbits.states.pet_state import PetState
from petbits.states.produto_state import ProdutoState
from petbits.states.prontuario_state import ProntuarioState
from petbits.states.servico_state import ServicoState

create_db_and_tables()

app = rx.App()

app.add_page(
    index,
    route="/",
    title="PetBits | Painel",
    on_load=DashboardState.load_dashboard,
)
app.add_page(
    clientes_page,
    route="/clientes",
    title="PetBits | Clientes",
    on_load=ClienteState.load_clientes,
)
app.add_page(
    pets_page,
    route="/pets",
    title="PetBits | Pets",
    on_load=PetState.load_pets,
)
app.add_page(
    agendamentos_page,
    route="/agendamentos",
    title="PetBits | Agendamentos",
    on_load=AgendamentoState.load_agendamentos,
)
app.add_page(
    prontuarios_page,
    route="/prontuarios",
    title="PetBits | Prontuários",
    on_load=ProntuarioState.load_prontuarios,
)
app.add_page(
    servicos_page,
    route="/servicos",
    title="PetBits | Serviços",
    on_load=ServicoState.load_servicos,
)
app.add_page(
    produtos_page,
    route="/produtos",
    title="PetBits | Produtos",
    on_load=ProdutoState.load_produtos,
)
app.add_page(
    pedidos_page,
    route="/pedidos",
    title="PetBits | Pedidos",
    on_load=PedidoState.load_pedidos,
)
app.add_page(
    funcionarios_page,
    route="/funcionarios",
    title="PetBits | Funcionários",
    on_load=FuncionarioState.load_funcionarios,
)
