"""Estado da loja do cliente (change `loja`).

O carrinho mora só no estado do Reflex: produto e quantidade. Preço, linha e
total que a tela mostra são **estimativas** a partir do catálogo carregado; o
valor que vale é o que o `POST pedidos` calcula no servidor e devolve.

Mesma guarda da área de cliente: sem sessão, ou com conta de equipe, nenhuma
requisição sai (change `porta-de-entrada`, D5).
"""

import reflex as rx

from petbits import agenda, xano
from petbits.states.auth_state import AuthState
from petbits.states.sessao import SemSessao
from petbits.xano import SessaoExpirada, XanoError

CATEGORIAS = {
    "racao": "Ração",
    "petisco": "Petisco",
    "brinquedo": "Brinquedo",
    "higiene": "Higiene",
    "acessorio": "Acessório",
    "medicamento": "Medicamento",
}
SITUACOES = {
    "pendente": "Aguardando pagamento",
    "pago": "Pago",
    "pronto_retirada": "Pronto para retirada",
    "enviado": "Enviado",
    "entregue": "Entregue",
    "cancelado": "Cancelado",
}
ENTREGAS = {"retirada": "Retirada na clínica", "endereco": "Entrega no endereço"}
PAGAMENTOS = {"na_loja": "Pagamento na loja", "online": "Pago online (simulado)"}


def reais(valor) -> str:
    try:
        texto = f"{float(valor):,.2f}"
    except (TypeError, ValueError):
        return "-"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


class LojaState(rx.State):
    produtos: list[dict] = []
    # produto_id (texto) -> quantidade. Chave texto porque o estado do Reflex
    # vai ao navegador como JSON.
    carrinho: dict[str, int] = {}

    entrega: str = "retirada"
    forma_pagamento: str = "na_loja"
    finalizando: bool = False
    enviando: bool = False

    pedidos: list[dict] = []

    carregando: bool = False
    ja_carregou: bool = False
    erro: str = ""
    aviso: str = ""

    def set_entrega(self, value: str):
        self.entrega = value

    def set_forma_pagamento(self, value: str):
        self.forma_pagamento = value

    def set_finalizando(self, value: bool):
        self.finalizando = value

    # --- derivados -------------------------------------------------------

    @rx.var
    def itens_do_carrinho(self) -> list[dict]:
        por_id = {str(p["id"]): p for p in self.produtos}
        itens = []
        for pid, qtd in self.carrinho.items():
            p = por_id.get(pid)
            if p:
                itens.append({
                    "id": pid,
                    "nome": p["nome"],
                    "quantidade": qtd,
                    "linha": reais(p["_preco"] * qtd),
                    "pode_mais": qtd < p["_estoque"],
                })
        return itens

    @rx.var
    def total_estimado(self) -> str:
        por_id = {str(p["id"]): p for p in self.produtos}
        return reais(sum(por_id[pid]["_preco"] * q for pid, q in self.carrinho.items()
                         if pid in por_id))

    @rx.var
    def quantidade_no_carrinho(self) -> int:
        return sum(self.carrinho.values())

    def limpar_dados(self):
        """Apaga tudo o que pertence a uma pessoa. Chamado pelo `sair`."""
        self.produtos = []
        self.carrinho = {}
        self.entrega = "retirada"
        self.forma_pagamento = "na_loja"
        self.finalizando = False
        self.enviando = False
        self.pedidos = []
        self.carregando = False
        self.ja_carregou = False
        self.erro = ""
        self.aviso = ""

    # --- sessão -----------------------------------------------------------

    async def _token(self) -> str:
        auth = await self.get_state(AuthState)
        if not auth.token:
            raise SemSessao()
        if xano.eh_equipe(auth.usuario_papel):
            raise SemSessao("/equipe")
        return auth.token

    async def _encerrar(self, erro: Exception):
        if isinstance(erro, SessaoExpirada):
            auth = await self.get_state(AuthState)
            auth._limpar(expirou=True)
        return rx.redirect(getattr(erro, "destino", "/entrar"))

    # --- loja ---------------------------------------------------------------

    async def carregar_loja(self):
        self.erro = ""
        self.carregando = True
        self.produtos = []
        try:
            token = await self._token()
            registros = await xano.produtos_da_loja(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            self.erro = str(erro)
            self.carregando = False
            self.ja_carregou = True
            return
        self.produtos = [
            {
                "id": p.get("id"),
                "nome": p.get("nome") or "-",
                "descricao": p.get("descricao") or "",
                "categoria": CATEGORIAS.get(p.get("categoria") or "", "-"),
                "marca": p.get("marca") or "",
                "unidade": p.get("unidade") or "",
                "preco": reais(p.get("preco")),
                "disponivel": f"{int(p.get('estoque') or 0)} disponível(is)",
                "_preco": float(p.get("preco") or 0),
                "_estoque": int(p.get("estoque") or 0),
            }
            for p in registros
        ]
        # O carrinho não pode apontar para produto que saiu da loja nem pedir
        # mais do que o estoque que acabou de chegar.
        estoque = {str(p["id"]): p["_estoque"] for p in self.produtos}
        self.carrinho = {pid: min(q, estoque[pid]) for pid, q in self.carrinho.items()
                         if estoque.get(pid, 0) > 0}
        self.carregando = False
        self.ja_carregou = True

    def adicionar(self, produto_id: int):
        pid = str(produto_id)
        estoque = next((p["_estoque"] for p in self.produtos if str(p["id"]) == pid), 0)
        atual = self.carrinho.get(pid, 0)
        if atual < estoque:
            self.carrinho = {**self.carrinho, pid: atual + 1}
        self.aviso = ""

    def tirar(self, produto_id: str):
        atual = self.carrinho.get(produto_id, 0)
        resto = {k: v for k, v in self.carrinho.items() if k != produto_id}
        if atual > 1:
            resto[produto_id] = atual - 1
        self.carrinho = resto

    def abrir_finalizacao(self):
        if self.carrinho:
            self.erro = ""
            self.finalizando = True

    async def finalizar(self):
        if not self.carrinho:
            return
        self.erro = ""
        self.enviando = True
        yield
        try:
            token = await self._token()
            itens = [{"produto_id": int(pid), "quantidade": q}
                     for pid, q in self.carrinho.items()]
            pedido = await xano.fazer_pedido(itens, self.entrega, self.forma_pagamento,
                                             token=token)
        except (SemSessao, SessaoExpirada) as erro:
            yield await self._encerrar(erro)
            return
        except XanoError as erro:
            self.erro = str(erro)
            return
        finally:
            # Mesmo motivo da change `entrada-sem-trava`.
            self.enviando = False

        self.carrinho = {}
        self.finalizando = False
        self.aviso = (
            f"Pedido nº {pedido.get('id')} feito: {reais(pedido.get('total'))} — "
            f"{SITUACOES.get(pedido.get('situacao') or '', '')}."
        )
        # O estoque mudou: a vitrine é recarregada.
        resultado = await self.carregar_loja()
        if resultado is not None:
            yield resultado

    # --- meus pedidos -------------------------------------------------------

    async def carregar_pedidos(self):
        self.erro = ""
        self.carregando = True
        self.pedidos = []
        try:
            token = await self._token()
            dados = await xano.meus_pedidos(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            self.erro = str(erro)
            self.carregando = False
            self.ja_carregou = True
            return
        itens_por_pedido: dict[int, list[dict]] = {}
        for i in dados.get("itens") or []:
            itens_por_pedido.setdefault(i.get("id_pedido"), []).append({
                "texto": f"{int(i.get('quantidade') or 0)} × {i.get('produto_nome') or '-'}",
                "linha": reais(i.get("valor_linha")),
            })
        self.pedidos = [
            {
                "id": p.get("id"),
                "quando": agenda.data_curta(p.get("created_at")),
                "situacao": SITUACOES.get(p.get("situacao") or "", "-"),
                "cancelado": p.get("situacao") == "cancelado",
                "entrega": ENTREGAS.get(p.get("entrega") or "", "-"),
                "endereco": p.get("endereco_entrega") or "",
                "pagamento": PAGAMENTOS.get(p.get("forma_pagamento") or "", "-"),
                "total": reais(p.get("total")),
                "itens": itens_por_pedido.get(p.get("id"), []),
            }
            for p in dados.get("pedidos") or []
        ]
        self.carregando = False
        self.ja_carregou = True
