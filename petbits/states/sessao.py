"""A guarda de sessão que os States de CRUD usam.

Por que a guarda mora aqui e não só no `on_load` da rota: `rx.redirect` é um
evento de frontend e **não cancela** o que já está na fila do backend. Um
`on_load=[carregar_sessao, load_clientes]` manda o redirect para o navegador,
mas o `load_clientes` roda assim mesmo — a requisição sai, e um visitante não
autenticado veria o erro cru (ou, pior, o dado). A barreira que de fato
funciona é o `return` antecipado dentro de cada `load_*`, e é isso que o mixin
abaixo torna barato.

`Sessao` é um mixin: não entra na árvore de estados, então os nove States
continuam sendo raízes independentes como sempre foram.
"""

import reflex as rx

from petbits.states.auth_state import AuthState
from petbits.xano import SessaoExpirada


class SemSessao(Exception):
    """O visitante não pode ver esta página. `destino` é para onde mandá-lo."""

    def __init__(self, destino: str):
        super().__init__(destino)
        self.destino = destino


class Sessao(rx.State, mixin=True):
    async def _token(self, *, admin: bool = True) -> str:
        """Token do usuário logado, barrando quem não pode estar ali.

        `admin=True` (o padrão) é para as nove telas da clínica. As telas do
        portal do tutor passam `admin=False`.
        """
        auth = await self.get_state(AuthState)
        if not auth.token:
            raise SemSessao("/login")
        if admin and not auth.eh_admin:
            raise SemSessao("/sem-permissao")
        return auth.token

    async def _encerrar(self, erro: Exception):
        """Trata os dois casos de sessão: bloqueio e token expirado."""
        if isinstance(erro, SessaoExpirada):
            auth = await self.get_state(AuthState)
            auth._limpar(expirou=True)
            return rx.redirect("/login")
        destino = getattr(erro, "destino", "/login")
        return rx.redirect(destino)
