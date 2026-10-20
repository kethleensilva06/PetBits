"""Estado da loja do cliente (change `loja`).

O carrinho guarda só produto e quantidade, no navegador, para sobreviver ao F5
(change `carrinho-guardado`). Preço, linha e
total que a tela mostra são **estimativas** a partir do catálogo carregado; o
valor que vale é o que o `POST pedidos` calcula no servidor e devolve.

Mesma guarda da área de cliente: sem sessão, ou com conta de equipe, nenhuma
requisição sai (change `porta-de-entrada`, D5).
"""

import reflex as rx

from petbits import agenda, carrinho as carrinho_guardado, etapas_do_pedido, rotulos, xano
from petbits.ilustracoes import imagem_do_produto, normalizar
from petbits.states.auth_state import AuthState
from petbits.states import sessao
from petbits.states.sessao import SemSessao
from petbits.xano import SessaoExpirada, XanoError

CATEGORIAS = rotulos.CATEGORIAS_PRODUTO
SITUACOES = rotulos.SITUACOES_PEDIDO
ENTREGAS = rotulos.ENTREGAS
PAGAMENTOS = rotulos.PAGAMENTOS
ORIGENS = rotulos.ORIGENS


def reais(valor) -> str:
    try:
        texto = f"{float(valor):,.2f}"
    except (TypeError, ValueError):
        return "-"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


# A ordem da loja (change `ordenar-a-loja`). "Em destaque" é a do catálogo.
ORDENS = ["Em destaque", "Menor preço", "Maior preço", "Nome (A–Z)"]


def ordenar_produtos(produtos: list[dict], ordem: str) -> list[dict]:
    if ordem == "Menor preço":
        return sorted(produtos, key=lambda p: p.get("_preco") or 0)
    if ordem == "Maior preço":
        return sorted(produtos, key=lambda p: p.get("_preco") or 0, reverse=True)
    if ordem == "Nome (A–Z)":
        return sorted(produtos, key=lambda p: normalizar(p.get("nome")))
    return list(produtos)


def filtrar_produtos(produtos: list[dict], busca: str, categoria: str) -> list[dict]:
    """Busca pelo nome (sem acento nem maiúscula) e filtro pelo rótulo da
    categoria; "" é "todas" (change `acabamentos-de-tela`, D4)."""
    termo = normalizar(busca)
    return [
        p for p in produtos
        if (not categoria or p.get("categoria") == categoria)
        and (not termo or termo in normalizar(p.get("nome")))
    ]


class LojaState(rx.State):
    produtos: list[dict] = []
    # produto_id (texto) -> quantidade. Chave texto porque o estado do Reflex
    # vai ao navegador como JSON.
    # No navegador, como a sessão (change `carrinho-guardado`, D1): sobrevive
    # ao F5, à aba nova e ao reinício do servidor. `carrinho` é derivado daqui.
    carrinho_salvo: str = rx.LocalStorage("", name="petbits_carrinho", sync=True)
    # O que a conferência com o estoque mudou no carrinho (change
    # `comprar-de-novo`, D2). Some na próxima mudança do carrinho.
    ajuste_carrinho: str = ""

    entrega: str = "retirada"
    forma_pagamento: str = "na_loja"
    finalizando: bool = False
    enviando: bool = False

    pedidos: list[dict] = []

    # Detalhe do produto (change `fotos-realistas`): o item vem da lista que
    # a loja já tem — abrir o detalhe não faz requisição.
    produto_aberto: dict = {}
    detalhe_aberto: bool = False
    qtd_detalhe: int = 1

    # Busca e filtro (change `acabamentos-de-tela`, D4): saem da lista que a
    # loja já carregou, sem requisição.
    busca: str = ""
    categoria_filtro: str = ""
    ordem: str = ORDENS[0]

    def set_busca(self, v: str):
        self.busca = v

    def set_categoria_filtro(self, v: str):
        self.categoria_filtro = "" if v == "Todas" else v

    def set_ordem(self, v: str):
        self.ordem = v if v in ORDENS else ORDENS[0]

    def limpar_filtros(self):
        self.busca = ""
        self.categoria_filtro = ""
        self.ordem = ORDENS[0]

    @rx.var
    def produtos_visiveis(self) -> list[dict]:
        return ordenar_produtos(
            filtrar_produtos(self.produtos, self.busca, self.categoria_filtro), self.ordem)

    @rx.var
    def categorias_da_loja(self) -> list[str]:
        """Só as categorias que têm produto à venda, na ordem dos rótulos."""
        presentes = {p.get("categoria") for p in self.produtos}
        return ["Todas"] + [c for c in CATEGORIAS.values() if c in presentes]

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

    def abrir_produto(self, produto: dict):
        self.produto_aberto = produto
        self.qtd_detalhe = 1
        self.detalhe_aberto = True

    @rx.var
    def pode_por_mais_no_aberto(self) -> int:
        """Quantas unidades ainda cabem: o estoque menos o que já está no carrinho."""
        estoque = int(self.produto_aberto.get("_estoque") or 0)
        return max(estoque - self.carrinho.get(str(self.produto_aberto.get("id", "")), 0), 0)

    def mais_um(self):
        if self.qtd_detalhe < self.pode_por_mais_no_aberto:
            self.qtd_detalhe += 1

    def menos_um(self):
        if self.qtd_detalhe > 1:
            self.qtd_detalhe -= 1

    def adicionar_do_detalhe(self):
        pid = str(self.produto_aberto.get("id", ""))
        quantos = min(self.qtd_detalhe, self.pode_por_mais_no_aberto)
        if pid and quantos > 0:
            self._gravar({**self.carrinho, pid: self.carrinho.get(pid, 0) + quantos})
            self.aviso = ""
            self.qtd_detalhe = 1
            return rx.toast.success(f"{quantos} no carrinho.")

    def set_detalhe_aberto(self, value: bool):
        self.detalhe_aberto = value

    # --- derivados -------------------------------------------------------

    @rx.var
    def carrinho(self) -> dict[str, int]:
        """{id do produto: quantidade}, lido com desconfiança do navegador (D2)."""
        return carrinho_guardado.ler(self.carrinho_salvo)

    def _gravar(self, novo: dict[str, int]):
        """Toda mudança do carrinho passa por aqui (D1)."""
        self.carrinho_salvo = carrinho_guardado.escrever(novo)
        self.ajuste_carrinho = ""

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
                    "preco": reais(p["_preco"]),
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

    @rx.var
    def quantidade_do_aberto(self) -> int:
        return self.carrinho.get(str(self.produto_aberto.get("id", "")), 0)

    def preparar_carga(self):
        """Primeiro evento do `on_load` (change `esqueletos-de-carregamento`).

        O carregador só manda o estado à tela quando termina; sem este passo,
        o "carregando" nunca chegava, e a tela mostrava o vazio até os dados
        virem. Sem requisição: só avisa a tela de que a carga começou.
        """
        self.erro = ""
        self.carregando = True
        self.ja_carregou = False

    @rx.var
    def mostrar_carregando(self) -> bool:
        """O mesmo de `PetState.mostrar_carregando`: carregando, ou ainda não
        carregado e sem erro."""
        return self.carregando or (not self.ja_carregou and not self.erro)

    def limpar_dados(self):
        """Apaga tudo o que pertence a uma pessoa. Chamado pelo `sair`."""
        self.produtos = []
        self._gravar({})
        self.entrega = "retirada"
        self.forma_pagamento = "na_loja"
        self.finalizando = False
        self.enviando = False
        self.pedidos = []
        self.produto_aberto = {}
        self.detalhe_aberto = False
        self.qtd_detalhe = 1
        self.busca = ""
        self.categoria_filtro = ""
        self.carregando = False
        self.ja_carregou = False
        self.erro = ""
        self.aviso = ""

    # --- sessão -----------------------------------------------------------

    async def _token(self) -> str:
        return await sessao.token_de_cliente(self)

    async def _encerrar(self, erro: Exception):
        return await sessao.encerrar(self, erro)

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
                "imagem": imagem_do_produto(p.get("nome"), p.get("categoria"), p.get("foto")),
                "marca": p.get("marca") or "",
                "unidade": p.get("unidade") or "",
                "preco": reais(p.get("preco")),
                # "28 em estoque", e não "28 disponível(is)" (change `loja-organizada`).
                "disponivel": f"{int(p.get('estoque') or 0)} em estoque",
                "_preco": float(p.get("preco") or 0),
                "_estoque": int(p.get("estoque") or 0),
            }
            for p in registros
        ]
        # O carrinho não pode apontar para produto que saiu da loja nem pedir
        # mais do que o estoque que acabou de chegar.
        estoque = {str(p["id"]): p["_estoque"] for p in self.produtos}
        # Vale também para o carrinho guardado, que pode ter dias (D3), e para
        # o pedido repetido, que pode ser antigo (change `comprar-de-novo`, D2).
        ajustado, aviso = carrinho_guardado.ajustar_ao_estoque(self.carrinho, estoque)
        if ajustado != self.carrinho:
            self._gravar(ajustado)
        self.ajuste_carrinho = aviso
        self.carregando = False
        self.ja_carregou = True

    def adicionar(self, produto_id: int):
        pid = str(produto_id)
        estoque = next((p["_estoque"] for p in self.produtos if str(p["id"]) == pid), 0)
        atual = self.carrinho.get(pid, 0)
        if atual < estoque:
            self._gravar({**self.carrinho, pid: atual + 1})
        self.aviso = ""

    def comprar_de_novo(self, pedido_id: int):
        """Os itens do pedido somados ao carrinho, e a loja (change
        `comprar-de-novo`). A loja confere o estoque ao abrir."""
        pedido = next((p for p in self.pedidos if p["id"] == pedido_id), None)
        if not pedido:
            return
        self._gravar(carrinho_guardado.somar(self.carrinho, pedido["_repetir"]))
        return [rx.redirect("/loja"),
                rx.toast.success(f"Itens do pedido nº {pedido_id} no carrinho.")]

    async def cancelar_pedido(self, pedido_id: int):
        """Cancela o próprio pedido; quem decide se pode é o backend."""
        self.erro = ""
        try:
            token = await self._token()
            await xano.cancelar_pedido(pedido_id, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except XanoError as erro:
            self.erro = str(erro)
            return
        await self.carregar_pedidos()
        return rx.toast.success(f"Pedido nº {pedido_id} cancelado. Os itens voltaram ao estoque.")

    def tirar(self, produto_id: str):
        atual = self.carrinho.get(produto_id, 0)
        resto = {k: v for k, v in self.carrinho.items() if k != produto_id}
        if atual > 1:
            resto[produto_id] = atual - 1
        self._gravar(resto)

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

        self._gravar({})
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
        # Produto e quantidade de cada item, para o Comprar de novo.
        repetir: dict[int, list[dict]] = {}
        for i in dados.get("itens") or []:
            repetir.setdefault(i.get("id_pedido"), []).append(
                {"id_produto": i.get("id_produto") or 0, "quantidade": i.get("quantidade") or 0})
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
                "origem": ORIGENS.get(p.get("origem") or "site", ""),
                "total": reais(p.get("total")),
                "itens": itens_por_pedido.get(p.get("id"), []),
                "_repetir": repetir.get(p.get("id"), []),
                # O botão só quando o backend aceitaria (change
                # `cliente-cancela-pedido`, D4): aguardando e sem pagamento.
                "pode_cancelar": p.get("situacao") == "pendente" and not p.get("pago_em"),
                # As etapas do caminho (change `linha-do-tempo-do-pedido`).
                "etapas": etapas_do_pedido.etapas(p.get("situacao") or "",
                                                  p.get("entrega") or "",
                                                  p.get("forma_pagamento") or "",
                                                  p.get("pago_em")),
            }
            for p in dados.get("pedidos") or []
        ]
        self.carregando = False
        self.ja_carregou = True
