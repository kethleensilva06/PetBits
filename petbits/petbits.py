"""PetBits — sistema de gestão para clínica veterinária e petshop.

As funcionalidades entram change por change, pelo fluxo do OpenSpec. Nenhuma
página deve aparecer aqui sem uma change correspondente em
`openspec/changes/` ou no histórico de `openspec/changes/archive/`.
"""

import reflex as rx

from petbits.pages.entrar import cadastro_page, entrar_page
from petbits.pages.inicio import inicio_page
from petbits.states.auth_state import AuthState
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
