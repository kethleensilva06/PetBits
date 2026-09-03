"""Estado e regras da página de Produtos."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import Produto


class ProdutoState(rx.State):
    produtos: list[dict] = []
    search: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    nome: str = ""
    categoria: str = ""
    marca: str = ""
    unidade: str = ""
    preco_venda: str = "0.00"

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_nome(self, value: str):
        self.nome = value

    def set_categoria(self, value: str):
        self.categoria = value

    def set_marca(self, value: str):
        self.marca = value

    def set_unidade(self, value: str):
        self.unidade = value

    def set_preco_venda(self, value: str):
        self.preco_venda = value

    @rx.var
    def filtered_produtos(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.produtos
        return [
            p
            for p in self.produtos
            if term in p["nome"].lower() or term in p["categoria"].lower()
        ]

    def load_produtos(self):
        with get_session() as session:
            produtos = session.exec(select(Produto).order_by(Produto.nome)).all()

        self.produtos = [
            {
                "id": p.id,
                "nome": p.nome,
                "categoria": p.categoria or "-",
                "marca": p.marca or "-",
                "unidade": p.unidade or "-",
                "preco_venda": f"{p.preco_venda:.2f}",
            }
            for p in produtos
        ]

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.categoria = ""
        self.marca = ""
        self.unidade = ""
        self.preco_venda = "0.00"
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, produto: dict):
        self.editing_id = produto["id"]
        self.nome = produto["nome"]
        self.categoria = produto["categoria"] if produto["categoria"] != "-" else ""
        self.marca = produto["marca"] if produto["marca"] != "-" else ""
        self.unidade = produto["unidade"] if produto["unidade"] != "-" else ""
        self.preco_venda = produto["preco_venda"]
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    def save(self):
        if not self.nome.strip():
            self.form_error = "Nome é obrigatório."
            return
        try:
            preco = float(self.preco_venda.replace(",", "."))
        except ValueError:
            self.form_error = "Preço inválido."
            return
        if preco < 0:
            self.form_error = "Preço não pode ser negativo."
            return

        with get_session() as session:
            if self.editing_id is None:
                session.add(
                    Produto(
                        nome=self.nome.strip(),
                        categoria=self.categoria.strip() or None,
                        marca=self.marca.strip() or None,
                        unidade=self.unidade.strip() or None,
                        preco_venda=preco,
                    )
                )
            else:
                produto = session.get(Produto, self.editing_id)
                produto.nome = self.nome.strip()
                produto.categoria = self.categoria.strip() or None
                produto.marca = self.marca.strip() or None
                produto.unidade = self.unidade.strip() or None
                produto.preco_venda = preco
                session.add(produto)
            session.commit()

        self.show_dialog = False
        self.load_produtos()

    def delete(self, produto_id: int):
        with get_session() as session:
            produto = session.get(Produto, produto_id)
            if produto is not None:
                session.delete(produto)
                session.commit()
        self.load_produtos()
