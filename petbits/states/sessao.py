"""A guarda de acesso que todo State privado usa.

Mora num módulo próprio porque passou a ter dois usuários. Duas classes
`SemSessao` em arquivos diferentes seriam tipos **diferentes**, e um
`except SemSessao` pegaria uma e deixaria a outra subir — o tipo de defeito
que só aparece quando alguém já está sem sessão.

**A guarda é o `raise` daqui, lido por um `return` antecipado dentro de cada
loader — não um `rx.redirect` no `on_load`.** `rx.redirect` é evento de
frontend e não cancela o que já está na fila do backend: o carregamento
enfileirado depois rodaria assim mesmo e a requisição sairia. Esconder a tela
sem impedir a requisição não esconde nada.
"""


class SemSessao(Exception):
    """Não há sessão válida para esta tela. `destino` é para onde mandar.

    Os dois destinos querem dizer coisas diferentes:

    - `/entrar/cliente` — não há sessão nenhuma;
    - `/inicio` — há sessão, mas não é de equipe, então a área da clínica não é
      para esta pessoa.

    O segundo caso é **conveniência de interface**. Quem protege é o backend,
    que lê o papel do banco a cada requisição e recusa com 403 mesmo que a
    tela seja forjada no armazenamento local.
    """

    def __init__(self, destino: str = "/entrar/cliente"):
        super().__init__(destino)
        self.destino = destino


async def token_de_cliente(state, sem_sessao: str = "/entrar/cliente") -> str:
    """O token de quem está na área de cliente — a guarda que `PetState`,
    `AgendaState` e `LojaState` repetiam (change `acabamentos`, D1).

    Levanta `SemSessao` **antes** de qualquer requisição:

    - sem sessão: para `sem_sessao` — mas, se a sessão acabou de EXPIRAR, para
      `/entrar/cliente`, onde está o aviso; quem roda depois de `carregar_sessao` não
      pode passar por cima dele;
    - conta de equipe: para `/equipe` — funcionário não usa a área de cliente
      (change `porta-de-entrada`).
    """
    from petbits import xano
    from petbits.states.auth_state import AuthState

    auth = await state.get_state(AuthState)
    if not auth.token:
        raise SemSessao("/entrar/cliente" if auth.sessao_expirou else sem_sessao)
    if xano.eh_equipe(auth.usuario_papel):
        raise SemSessao("/equipe")
    return auth.token


async def encerrar(state, erro: Exception):
    """Redireciona depois de uma recusa de sessão. Só a credencial vencida
    (`SessaoExpirada`) limpa a sessão — e marca o aviso; `SemSessao` só leva
    ao destino dela."""
    import reflex as rx

    from petbits.states.auth_state import AuthState
    from petbits.xano import SessaoExpirada

    if isinstance(erro, SessaoExpirada):
        auth = await state.get_state(AuthState)
        auth._limpar(expirou=True)
    return rx.redirect(getattr(erro, "destino", "/entrar/cliente"))
