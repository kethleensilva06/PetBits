"""Estado e regras da página de Pedidos e seus itens."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import STATUS_PEDIDO, Cliente, ItensPedido, Pedido, Produto


class PedidoState(rx.State):
    pedidos: list[dict] = []
    cliente_options: list[Cliente] = []
    produto_options: list[Produto] = []
    search: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    id_cliente: str = ""
    status: str = STATUS_PEDIDO[0]

    show_itens_dialog: bool = False
    selected_pedido_id: Optional[int] = None
    selected_pedido_cliente: str = ""
    itens: list[dict] = []
    itens_total: str = "0.00"
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

    def load_pedidos(self):
        with get_session() as session:
            pedidos = session.exec(
                select(Pedido).order_by(Pedido.data_pedido.desc())
            ).all()
            self.cliente_options = list(
                session.exec(select(Cliente).order_by(Cliente.nome)).all()
            )
            self.produto_options = list(
                session.exec(select(Produto).order_by(Produto.nome)).all()
            )

        clientes_by_id = {c.id: c.nome for c in self.cliente_options}
        self.pedidos = [
            {
                "id": p.id,
                "cliente_nome": clientes_by_id.get(p.id_cliente, "Cliente removido"),
                "id_cliente": p.id_cliente,
                "data_pedido": p.data_pedido.strftime("%d/%m/%Y %H:%M"),
                "status": p.status,
                "valor_total": f"{p.valor_total:.2f}",
            }
            for p in pedidos
        ]

    def open_new(self):
        self.editing_id = None
        self.id_cliente = str(self.cliente_options[0].id) if self.cliente_options else ""
        self.status = STATUS_PEDIDO[0]
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

    def save(self):
        if not self.id_cliente:
            self.form_error = "Selecione o cliente do pedido."
            return

        with get_session() as session:
            if self.editing_id is None:
                session.add(
                    Pedido(id_cliente=int(self.id_cliente), status=self.status)
                )
            else:
                pedido = session.get(Pedido, self.editing_id)
                pedido.id_cliente = int(self.id_cliente)
                pedido.status = self.status
                session.add(pedido)
            session.commit()

        self.show_dialog = False
        self.load_pedidos()

    def delete(self, pedido_id: int):
        with get_session() as session:
            for item in session.exec(
                select(ItensPedido).where(ItensPedido.id_pedido == pedido_id)
            ).all():
                session.delete(item)
            pedido = session.get(Pedido, pedido_id)
            if pedido is not None:
                session.delete(pedido)
            session.commit()
        self.load_pedidos()

    def open_itens(self, pedido: dict):
        self.selected_pedido_id = pedido["id"]
        self.selected_pedido_cliente = pedido["cliente_nome"]
        self.item_id_produto = (
            str(self.produto_options[0].id) if self.produto_options else ""
        )
        self.item_quantidade = "1"
        self.item_error = ""
        self.show_itens_dialog = True
        self.load_itens()

    def close_itens(self):
        self.show_itens_dialog = False

    def load_itens(self):
        if self.selected_pedido_id is None:
            self.itens = []
            self.itens_total = "0.00"
            return

        with get_session() as session:
            itens = session.exec(
                select(ItensPedido).where(
                    ItensPedido.id_pedido == self.selected_pedido_id
                )
            ).all()
            produtos_by_id = {
                p.id: p.nome
                for p in session.exec(select(Produto)).all()
            }

        self.itens = [
            {
                "id": i.id,
                "produto_nome": produtos_by_id.get(i.id_produto, "Produto removido"),
                "quantidade": i.quantidade,
                "valor_unitario": f"{i.valor_unitario:.2f}",
                "valor_total": f"{i.valor_total:.2f}",
            }
            for i in itens
        ]
        self.itens_total = f"{sum(i.valor_total for i in itens):.2f}"

    def add_item(self):
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

        with get_session() as session:
            produto = session.get(Produto, int(self.item_id_produto))
            if produto is None:
                self.item_error = "Produto não encontrado."
                return
            session.add(
                ItensPedido(
                    id_pedido=self.selected_pedido_id,
                    id_produto=produto.id,
                    quantidade=quantidade,
                    valor_unitario=produto.preco_venda,
                    valor_total=quantidade * produto.preco_venda,
                )
            )
            session.commit()

        self.item_error = ""
        self.item_quantidade = "1"
        self.load_itens()
        self._recalcular_total()

    def remove_item(self, item_id: int):
        with get_session() as session:
            item = session.get(ItensPedido, item_id)
            if item is not None:
                session.delete(item)
                session.commit()
        self.load_itens()
        self._recalcular_total()

    def _recalcular_total(self):
        """Atualiza o valor_total do pedido a partir da soma dos seus itens."""
        if self.selected_pedido_id is None:
            return

        with get_session() as session:
            itens = session.exec(
                select(ItensPedido).where(
                    ItensPedido.id_pedido == self.selected_pedido_id
                )
            ).all()
            pedido = session.get(Pedido, self.selected_pedido_id)
            if pedido is not None:
                pedido.valor_total = sum(i.valor_total for i in itens)
                session.add(pedido)
                session.commit()

        self.load_pedidos()
