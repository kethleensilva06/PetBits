"""Estado e regras da página de Pedidos e seus itens."""

from datetime import datetime
from typing import Optional

import reflex as rx

from petbits import models
from petbits.states.conversores import formatar_data_hora, formatar_moeda
from petbits.xano import XanoError


class PedidoState(rx.State):
    pedidos: list[dict] = []
    cliente_options: list[dict] = []
    produto_options: list[dict] = []
    search: str = ""
    load_error: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    id_cliente: str = ""
    status: str = models.STATUS_PEDIDO[0]

    show_itens_dialog: bool = False
    selected_pedido_id: Optional[int] = None
    selected_pedido_cliente: str = ""
    itens: list[dict] = []
    itens_total: str = "0.00"
    itens_total_valor: float = 0.0
    item_error: str = ""
    item_id_produto: str = ""
    item_quantidade: str = "1"

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_show_itens_dialog(self, value: bool):
        self.show_itens_dialog = value

    def set_id_cliente(self, value: str):
        self.id_cliente = value

    def set_status(self, value: str):
        self.status = value

    def set_item_id_produto(self, value: str):
        self.item_id_produto = value

    def set_item_quantidade(self, value: str):
        self.item_quantidade = value

    @rx.var
    def filtered_pedidos(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.pedidos
        return [
            p
            for p in self.pedidos
            if term in p["cliente_nome"].lower() or term in p["status"].lower()
        ]

    async def load_pedidos(self):
        self.load_error = ""
        try:
            pedidos = await models.pedidos.listar()
            clientes = await models.clientes.listar()
            produtos = await models.produtos.listar()
        except XanoError as erro:
            self.pedidos = []
            self.cliente_options = []
            self.produto_options = []
            self.load_error = str(erro)
            return

        self.cliente_options = [
            {"id": c.get("id"), "nome": c.get("nome") or ""}
            for c in sorted(clientes, key=lambda c: (c.get("nome") or "").lower())
        ]
        self.produto_options = [
            {
                "id": p.get("id"),
                "nome": p.get("nome") or "",
                "preco_venda": float(p.get("preco_venda") or 0),
            }
            for p in sorted(produtos, key=lambda p: (p.get("nome") or "").lower())
        ]

        clientes_by_id = {c["id"]: c["nome"] for c in self.cliente_options}
        self.pedidos = [
            {
                "id": p.get("id"),
                "cliente_nome": clientes_by_id.get(
                    p.get("id_cliente"), "Cliente removido"
                ),
                "id_cliente": p.get("id_cliente"),
                "data_pedido": formatar_data_hora(p.get("data_pedido")),
                "status": p.get("status") or "",
                "valor_total": formatar_moeda(p.get("valor_total")),
            }
            for p in sorted(
                pedidos, key=lambda p: p.get("data_pedido") or 0, reverse=True
            )
        ]

    def open_new(self):
        self.editing_id = None
        self.id_cliente = (
            str(self.cliente_options[0]["id"]) if self.cliente_options else ""
        )
        self.status = models.STATUS_PEDIDO[0]
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, pedido: dict):
        self.editing_id = pedido["id"]
        self.id_cliente = str(pedido["id_cliente"])
        self.status = pedido["status"]
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    async def save(self):
        if not self.id_cliente:
            self.form_error = "Selecione o cliente do pedido."
            return

        dados = {
            "id_cliente": int(self.id_cliente),
            "status": self.status,
        }

        try:
            if self.editing_id is None:
                # O Xano não preenche estes campos sozinho: o pedido nasce com
                # a data do momento e o total zerado, que os itens recalculam.
                dados["data_pedido"] = datetime.now().isoformat()
                dados["valor_total"] = 0.0
                await models.pedidos.criar(dados)
            else:
                await models.pedidos.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_pedidos()

    async def delete(self, pedido_id: int):
        try:
            # O Xano não tem ON DELETE CASCADE: os itens saem antes do pedido.
            for item in await models.itens_pedido.listar_por("id_pedido", pedido_id):
                item_id = item.get("id")
                if item_id is not None:
                    await models.itens_pedido.remover(item_id)
            await models.pedidos.remover(pedido_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_pedidos()

    async def open_itens(self, pedido: dict):
        self.selected_pedido_id = pedido["id"]
        self.selected_pedido_cliente = pedido["cliente_nome"]
        self.item_id_produto = (
            str(self.produto_options[0]["id"]) if self.produto_options else ""
        )
        self.item_quantidade = "1"
        self.item_error = ""
        self.show_itens_dialog = True
        await self.load_itens()

    def close_itens(self):
        self.show_itens_dialog = False

    async def load_itens(self):
        if self.selected_pedido_id is None:
            self.itens = []
            self.itens_total = "0.00"
            self.itens_total_valor = 0.0
            return

        try:
            itens = await models.itens_pedido.listar_por(
                "id_pedido", self.selected_pedido_id
            )
        except XanoError as erro:
            self.itens = []
            self.itens_total = "0.00"
            self.itens_total_valor = 0.0
            self.item_error = str(erro)
            return

        produtos_by_id = {
            p.get("id"): p.get("nome") or "" for p in self.produto_options
        }
        self.itens = [
            {
                "id": i.get("id"),
                "produto_nome": produtos_by_id.get(
                    i.get("id_produto"), "Produto removido"
                ),
                "quantidade": i.get("quantidade") or 0,
                "valor_unitario": formatar_moeda(i.get("valor_unitario")),
                "valor_total": formatar_moeda(i.get("valor_total")),
            }
            for i in sorted(itens, key=lambda i: i.get("id") or 0)
        ]
        self.itens_total_valor = sum(float(i.get("valor_total") or 0) for i in itens)
        self.itens_total = formatar_moeda(self.itens_total_valor)

    async def add_item(self):
        if self.selected_pedido_id is None or not self.item_id_produto:
            self.item_error = "Selecione um produto."
            return
        try:
            quantidade = int(self.item_quantidade)
        except ValueError:
            self.item_error = "Quantidade inválida."
            return
        if quantidade <= 0:
            self.item_error = "Quantidade deve ser maior que zero."
            return

        id_produto = int(self.item_id_produto)
        produto = next(
            (p for p in self.produto_options if p.get("id") == id_produto), None
        )
        if produto is None:
            self.item_error = "Produto não encontrado."
            return

        valor_unitario = float(produto.get("preco_venda") or 0)
        dados = {
            "id_pedido": self.selected_pedido_id,
            "id_produto": id_produto,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "valor_total": quantidade * valor_unitario,
        }

        try:
            await models.itens_pedido.criar(dados)
        except XanoError as erro:
            self.item_error = str(erro)
            return

        self.item_error = ""
        self.item_quantidade = "1"
        await self.load_itens()
        await self._recalcular_total()

    async def remove_item(self, item_id: int):
        try:
            await models.itens_pedido.remover(item_id)
        except XanoError as erro:
            self.item_error = str(erro)
            return
        await self.load_itens()
        await self._recalcular_total()

    async def _recalcular_total(self):
        """Atualiza o valor_total do pedido a partir da soma dos seus itens."""
        if self.selected_pedido_id is None:
            return

        try:
            # A soma sai de uma leitura própria, sobre os valores crus do Xano:
            # se a listagem falhar, o total gravado não é zerado por engano.
            itens = await models.itens_pedido.listar_por(
                "id_pedido", self.selected_pedido_id
            )
            total = float(sum(float(i.get("valor_total") or 0) for i in itens))

            # O endpoint de edição do Xano grava todos os campos que recebe,
            # então o pedido é reenviado inteiro: mandar só o valor_total
            # apagaria id_cliente e status.
            pedido = await models.pedidos.obter(self.selected_pedido_id)
            if pedido is None:
                self.item_error = "Pedido não encontrado no Xano."
                return
            await models.pedidos.atualizar(
                self.selected_pedido_id,
                {
                    "id_cliente": pedido.get("id_cliente"),
                    "status": pedido.get("status"),
                    "valor_total": total,
                },
            )
        except XanoError as erro:
            self.item_error = str(erro)
            return

        self.itens_total_valor = total
        self.itens_total = formatar_moeda(total)
        await self.load_pedidos()
