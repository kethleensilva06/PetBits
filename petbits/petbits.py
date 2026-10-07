"""PetBits — sistema de gestão para clínica veterinária e petshop.

As funcionalidades entram change por change, pelo fluxo do OpenSpec. Nenhuma
página deve aparecer aqui sem uma change correspondente em
`openspec/changes/` ou no histórico de `openspec/changes/archive/`.
"""

import reflex as rx

from petbits.pages.agenda import agenda_page
from petbits.pages.entrar import cadastro_page, entrar_page
from petbits.pages.equipe import (
    agenda_equipe_page,
    animais_page,
    colaboradores_page,
    painel_page,
    servicos_page,
    tutores_page,
)
from petbits.pages.inicio import inicio_page
from petbits.states.agenda_state import AgendaState
from petbits.states.auth_state import AuthState
from petbits.states.equipe_state import EquipeState
from petbits.states.pet_state import PetState

app = rx.App()

# Rota privada. O `on_load` é a guarda: `carregar_sessao` devolve um
# redirecionamento e **retorna antes** de qualquer chamada ao Xano quando não
# há sessão. Pôr só um `rx.redirect` aqui não bastaria — ele é evento de
# frontend e não cancela o que já está na fila do backend.
app.add_page(
    inicio_page,
    route="/",
    title="PetBits",
    on_load=[AuthState.carregar_sessao, PetState.carregar],
)

# Agenda do tutor (change `agendamento`). Mesma guarda da casa: sem sessão,
# `AgendaState._token` levanta antes de qualquer requisição.
app.add_page(
    agenda_page,
    route="/agenda",
    title="PetBits | Agendar",
    on_load=[AuthState.carregar_sessao, AgendaState.carregar],
)

# Área da clínica. Cada tela tem o seu próprio carregamento, e nenhuma
# carrega as outras: o painel traz só contadores, e a lista de cada área vem
# quando alguém clica nela. As quatro listas de uma vez custariam metade do
# orçamento de requisições da instância numa única abertura de tela.
#
# A guarda real é o retorno antecipado dentro de cada loader — sem conta de
# equipe, nenhuma requisição de dado da clínica chega a sair. O `rx.redirect`
# sozinho não bastaria: ele é evento de frontend e não cancela o que já está
# na fila do backend.
for rota, pagina, titulo, carregar in (
    ("/equipe", painel_page, "Painel", EquipeState.carregar_painel),
    ("/equipe/agenda", agenda_equipe_page, "Agenda", EquipeState.carregar_agenda),
    ("/equipe/colaboradores", colaboradores_page, "Colaboradores",
     EquipeState.carregar_colaboradores),
    ("/equipe/servicos", servicos_page, "Serviços", EquipeState.carregar_servicos),
    ("/equipe/tutores", tutores_page, "Tutores", EquipeState.carregar_tutores),
    ("/equipe/animais", animais_page, "Animais", EquipeState.carregar_animais),
):
    app.add_page(
        pagina,
        route=rota,
        title=f"PetBits | {titulo}",
        on_load=[AuthState.carregar_sessao, carregar],
    )

# Portas de entrada. `redirecionar_se_logado` evita mostrar o formulário a
# quem já entrou: voltar para cá por engano e ver campos vazios passa a
# impressão de que a sessão caiu.
app.add_page(
    entrar_page,
    route="/entrar",
    title="PetBits | Entrar",
    on_load=AuthState.redirecionar_se_logado,
)
app.add_page(
    cadastro_page,
    route="/cadastro",
    title="PetBits | Criar conta",
    on_load=AuthState.redirecionar_se_logado,
)
